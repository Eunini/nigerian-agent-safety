import json

import pytest

from safety.report import paired_guard_effect
from safety.run import validate_main_items


def test_paired_guard_changes_are_aggregate_only_and_exclude_missing_judgments():
    common = {
        "model": "test",
        "revision": "v1",
        "language": "yor",
        "mode": "agent",
        "kind": "harmful",
        "judge_status": "ok",
        "refusal": False,
        "harmful_tool_use": False,
        "input": "PRIVATE-CANARY",
        "text": "PRIVATE-CANARY",
    }
    records = []
    for i in range(8):
        records.extend(
            [
                {**common, "item_id": str(i), "guard": False, "harmful_completion": True},
                {**common, "item_id": str(i), "guard": True, "harmful_completion": False},
            ]
        )
    records.append({**common, "item_id": "missing", "guard": False, "harmful_completion": True})
    result = paired_guard_effect(records, repetitions=1000)[0]
    assert "PRIVATE-CANARY" not in json.dumps(result)
    assert result["paired_items"] == 8 and result["items_with_any_judgment"] == 9
    assert result["harmful_completion"]["difference_guard_minus_unguarded"] == -1
    assert result["harmful_completion"]["paired_bootstrap_ci95"] == [-1, -1]
    assert result["harmful_completion"]["mcnemar_exact_two_sided_p"] == pytest.approx(2 / 256)
    assert result["partial"]


def test_native_review_sample_cannot_be_run_as_a_full_study():
    with pytest.raises(ValueError, match="100 harmful"):
        validate_main_items([{"id": "one", "language": "yor", "kind": "benign"}])
