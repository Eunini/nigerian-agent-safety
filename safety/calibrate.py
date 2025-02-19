import argparse
import csv
import json
from pathlib import Path

from safety.io import rows
from safety.review import LABELS


def agreement(human, automatic):
    if not human or len(human) != len(automatic):
        raise ValueError("Need nonempty paired labels")
    n = len(human)
    observed = sum(a == b for a, b in zip(human, automatic, strict=True)) / n
    human_positive, auto_positive = sum(human) / n, sum(automatic) / n
    chance = human_positive * auto_positive + (1 - human_positive) * (1 - auto_positive)
    return {
        "n": n,
        "agreement": observed,
        "cohen_kappa": (observed - chance) / (1 - chance) if chance < 1 else None,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--judged", required=True)
    p.add_argument("--labels", required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    automatic = {r["case_id"]: r for r in rows(a.judged) if r.get("judge_status") == "ok"}
    with open(a.labels) as stream:
        human = list(csv.DictReader(stream))
    if len(human) < 100 or len({r["case_id"] for r in human}) != len(human):
        raise ValueError("Need at least 100 unique, independently human-labelled outputs")
    result = {}
    for label in LABELS:
        if any(r[label] not in {"true", "false"} or not r.get("reviewer") for r in human):
            raise ValueError("Fill each label with true/false and record a reviewer")
        result[label] = agreement(
            [r[label] == "true" for r in human], [automatic[r["case_id"]][label] for r in human]
        )
    a.out.write_text(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
