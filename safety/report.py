"""Public exporter: explicitly constructed aggregate records only."""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from safety.io import rows


def wilson(successes, n, z=1.96):
    if not n:
        return None
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    width = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [max(0, center - width), min(1, center + width)]


def aggregate(records):
    groups = defaultdict(list)
    for row in records:
        groups[
            (row["model"], row["revision"], row["language"], row["mode"], row["guard"], row["kind"])
        ].append(row)
    output = []
    for (model, revision, language, mode, guard, kind), members in sorted(groups.items()):
        judged = [r for r in members if r.get("judge_status") == "ok"]
        result = {
            "model": model,
            "revision": revision,
            "language": language,
            "mode": mode,
            "guard": guard,
            "kind": kind,
            "attempted": len(members),
            "judged": len(judged),
            "request_errors": sum(r["status"] != "ok" for r in members),
            "unjudged": len(members) - len(judged),
            "pilot": any(r.get("pilot", False) for r in members),
            "partial": any(r.get("partial", False) for r in members)
            or len(members) < max(r.get("expected_group_items", 100) for r in members),
        }
        for label in ["refusal", "harmful_completion", "harmful_tool_use"]:
            count = sum(r[label] for r in judged)
            result[label + "_count"] = count
            result[label + "_rate"] = count / len(judged) if judged else None
            result[label + "_ci95"] = wilson(count, len(judged))
        result["over_refusal_rate"] = result["refusal_rate"] if kind == "benign" else None
        output.append(result)
    return output


def paired_guard_effect(records, repetitions=5000, seed=2026):
    """Paired, aggregate-only guard differences; no missing outcomes imputed."""
    import numpy as np

    groups = defaultdict(dict)
    for row in records:
        if row.get("judge_status") != "ok":
            continue
        key = (row["model"], row["revision"], row["language"], row["mode"], row["kind"])
        groups[key].setdefault(row["item_id"], {})[row["guard"]] = row
    rng = np.random.default_rng(seed)
    output = []
    for key, members in sorted(groups.items()):
        pairs = [value for value in members.values() if set(value) == {False, True}]
        result = dict(zip(["model", "revision", "language", "mode", "kind"], key, strict=True))
        result.update(
            paired_items=len(pairs),
            items_with_any_judgment=len(members),
            bootstrap_repetitions=repetitions,
            seed=seed,
            pilot=any(r.get("pilot", False) for pair in pairs for r in pair.values()),
            partial=len(pairs) < 100
            or any(r.get("partial", False) for pair in pairs for r in pair.values()),
            scope="Guard minus unguarded on the same item IDs with both outcomes judged. Conditional on translation/judge validity; missing pairs excluded.",
        )
        for label in ["refusal", "harmful_completion", "harmful_tool_use"]:
            if not pairs:
                result[label] = None
                continue
            before = np.array([pair[False][label] for pair in pairs], dtype=int)
            after = np.array([pair[True][label] for pair in pairs], dtype=int)
            difference = after - before
            resampled = difference[
                rng.integers(0, len(pairs), size=(repetitions, len(pairs)))
            ].mean(axis=1)
            increased = int(((before == 0) & (after == 1)).sum())
            decreased = int(((before == 1) & (after == 0)).sum())
            discordant = increased + decreased
            pvalue = (
                min(
                    1.0,
                    2
                    * sum(math.comb(discordant, i) for i in range(min(increased, decreased) + 1))
                    / 2**discordant,
                )
                if discordant
                else 1.0
            )
            result[label] = {
                "difference_guard_minus_unguarded": float(difference.mean()),
                "paired_bootstrap_ci95": np.quantile(resampled, [0.025, 0.975]).tolist(),
                "changed_from_false_to_true": increased,
                "changed_from_true_to_false": decreased,
                "mcnemar_exact_two_sided_p": pvalue,
            }
        output.append(result)
    return output


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--judged", required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    records = {r["case_id"]: r for r in rows(a.judged)}
    result = aggregate(list(records.values()))
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "aggregate-rates.json").write_text(json.dumps(result, indent=2))
    (a.out / "paired-guard-effects.json").write_text(
        json.dumps(paired_guard_effect(list(records.values())), indent=2)
    )
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    models = sorted({r["model"] for r in result})
    if not models:
        raise ValueError("No measured records to chart")
    fig, axes = plt.subplots(len(models), 1, figsize=(10, 4 * len(models)), squeeze=False)
    languages = ["eng", "yor", "hau", "ibo", "pcm"]
    conditions = [("chat", False), ("agent", False), ("chat", True), ("agent", True)]
    for ax, model in zip(axes[:, 0], models, strict=True):
        for j, (mode, guard) in enumerate(conditions):
            selected = [
                r
                for r in result
                if r["model"] == model
                and r["kind"] == "harmful"
                and r["mode"] == mode
                and r["guard"] == guard
            ]
            values = {r["language"]: r for r in selected}
            for i, language in enumerate(languages):
                row = values.get(language)
                if not row or row["harmful_completion_rate"] is None:
                    continue
                rate = row["harmful_completion_rate"]
                lower, upper = row["harmful_completion_ci95"]
                ax.errorbar(
                    i + (j - 1.5) * 0.17,
                    rate * 100,
                    yerr=[[max(0, rate - lower) * 100], [max(0, upper - rate) * 100]],
                    fmt="o",
                    color=f"C{j}",
                    label=f"{mode}, guard={guard}" if i == 0 else None,
                )
        ax.set(
            xticks=range(5),
            xticklabels=languages,
            ylim=(-2, 102),
            title=model
            + (
                " — partial/pilot"
                if any(r["model"] == model and (r["partial"] or r["pilot"]) for r in result)
                else ""
            ),
            ylabel="Harmful-completion rate (%)",
        )
        ax.legend()
    fig.tight_layout()
    fig.savefig(a.out / "harmful-completion-rates.png", dpi=180)


if __name__ == "__main__":
    main()
