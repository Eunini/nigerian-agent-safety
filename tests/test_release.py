import json
import subprocess
from pathlib import Path

import pytest

from safety.io import private_stream


def test_private_text_cannot_be_written_to_a_public_report():
    with pytest.raises(ValueError):
        private_stream("report/accidental-public-output.jsonl", "w")


def test_sensitive_artifacts_are_not_tracked():
    root = Path(__file__).resolve().parents[1]
    if not (root / ".git").exists():
        pytest.skip("Repository not initialized yet")
    files = subprocess.check_output(
        ["git", "ls-files", "data/raw", "runs/private", "configs/local.json"], cwd=root, text=True
    )
    assert files.strip() == ""
    # The public example is configuration/schema only, with no embedded keys.
    config = json.loads((root / "configs/example.json").read_text())
    assert "key" not in config
