import json

import pytest

from safety.agent import interact
from safety.calibrate import agreement
from safety.report import aggregate, wilson
from safety.score import validate_judgment
from safety.tools import InertTools


def test_tools_are_inert_even_for_executable_arguments(tmp_path):
    victim = tmp_path / "must-not-exist"
    tools = InertTools()
    tools.call("run_code", {"language": "python", "code": f"open({str(victim)!r}, 'w').write('x')"})
    tools.call("write_file", {"path": str(victim), "content": "secret"})
    assert not victim.exists()
    assert all(r["executed"] is False for r in tools.events)
    assert "secret" not in json.dumps(tools.events)
    with pytest.raises(ValueError):
        tools.call("shell", {})


def test_agent_calls_only_stubs_and_finishes(tmp_path):
    path = tmp_path / "never-written"

    class Client:
        n = 0

        def complete(self, messages, tools=None):
            self.n += 1
            if self.n == 1:
                return {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "one",
                            "type": "function",
                            "function": {
                                "name": "write_file",
                                "arguments": json.dumps({"path": str(path), "content": "hello"}),
                            },
                        }
                    ],
                }
            return {"role": "assistant", "content": "Done"}

    result = interact(Client(), "a benign request", "agent")
    assert len(result["tools"]) == 1
    assert result["termination"] == "completed"
    assert not path.exists()


def test_strict_judge_does_not_accept_string_booleans():
    with pytest.raises(ValueError):
        validate_judgment(
            {"refusal": "false", "harmful_completion": False, "harmful_tool_use": False}
        )
    assert validate_judgment(
        {"refusal": True, "harmful_completion": False, "harmful_tool_use": False}
    )["refusal"]


def test_export_drops_raw_content_and_separates_missing_judgments():
    record = {
        "model": "test",
        "revision": "v1",
        "language": "yor",
        "mode": "agent",
        "guard": False,
        "kind": "harmful",
        "status": "ok",
        "judge_status": "ok",
        "refusal": False,
        "harmful_completion": True,
        "harmful_tool_use": False,
        "input": "NEVER-PUBLISH-ME",
        "text": "NEVER-PUBLISH-ME",
    }
    result = aggregate([record, {**record, "status": "error", "judge_status": "error"}])[0]
    assert "NEVER-PUBLISH-ME" not in json.dumps(result)
    assert result["judged"] == 1 and result["unjudged"] == 1
    assert result["harmful_completion_rate"] == 1
    assert wilson(0, 0) is None
    assert wilson(0, 100)[1] > 0


def test_human_agreement():
    assert agreement([True, False], [True, False])["cohen_kappa"] == 1
    assert agreement([True, True], [True, True])["cohen_kappa"] is None
