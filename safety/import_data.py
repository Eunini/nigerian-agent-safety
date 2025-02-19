"""Import restricted local benchmark text; stdout contains counts and hashes only."""

import argparse
import csv
import io
import json
import random
import urllib.request
from collections import defaultdict
from pathlib import Path

from safety.io import digest, private_stream

HARM_REV = "8e1604d1171fe8a48d8febecd22f600e462bdcdd"
XS_REV = "d7bb5bd738c1fcbc36edd83d5e7d1b71a3e2d84d"
HARM_URL = f"https://raw.githubusercontent.com/centerforaisafety/HarmBench/{HARM_REV}/data/behavior_datasets/harmbench_behaviors_text_all.csv"
XS_URL = (
    f"https://raw.githubusercontent.com/paul-rottger/exaggerated-safety/{XS_REV}/xstest_prompts.csv"
)


def download(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return list(csv.DictReader(io.StringIO(response.read().decode())))


def balanced(candidates, n, seed=2026):
    groups = defaultdict(list)
    for row in candidates:
        groups[row["category"]].append(row)
    rng = random.Random(seed)
    for group in groups.values():
        rng.shuffle(group)
    selected = []
    while len(selected) < n:
        progress = False
        for category in sorted(groups):
            if groups[category] and len(selected) < n:
                selected.append(groups[category].pop())
                progress = True
        if not progress:
            raise ValueError("Requested more unique examples than available")
    return selected


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--out", type=Path, default=Path("data/raw/english.jsonl"))
    a = p.parse_args()
    harmful = [
        {
            "id": "hb:" + r["BehaviorID"],
            "kind": "harmful",
            "text": r["Behavior"],
            "category": r["SemanticCategory"],
            "source": "HarmBench",
            "source_revision": HARM_REV,
        }
        for r in download(HARM_URL)
        if r["FunctionalCategory"] == "standard"
    ]
    benign = [
        {
            "id": "xs:" + str(r["id"]),
            "kind": "benign",
            "text": r["prompt"],
            "category": r["type"],
            "source": "XSTest",
            "source_revision": XS_REV,
        }
        for r in download(XS_URL)
        if r["label"] == "safe"
    ]
    selected = balanced(harmful, a.n) + balanced(benign, a.n)
    with private_stream(a.out, "w") as stream:
        for row in selected:
            stream.write(
                json.dumps(
                    {**row, "language": "eng", "source_sha256": digest(row["text"])},
                    ensure_ascii=False,
                )
                + "\n"
            )
    print(json.dumps({"harmful": a.n, "benign": a.n, "selection_sha256": digest(selected)}))


if __name__ == "__main__":
    main()
