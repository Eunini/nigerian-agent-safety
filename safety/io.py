import hashlib
import json
import os
from pathlib import Path


def rows(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


def digest(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


def private_stream(path, mode="a"):
    path = Path(path)
    root = Path(__file__).resolve().parents[1]
    allowed = [root / "data/raw", root / "runs/private"]
    if not any(path.resolve().is_relative_to(folder.resolve()) for folder in allowed):
        raise ValueError("Private text must stay under data/raw/ or runs/private/")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | (os.O_APPEND if mode == "a" else os.O_TRUNC), 0o600
    )
    os.fchmod(descriptor, 0o600)
    return os.fdopen(descriptor, mode)
