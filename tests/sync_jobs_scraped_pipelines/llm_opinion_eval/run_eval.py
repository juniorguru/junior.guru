"""Offline precision/recall eval for llm_opinion.process().

See README.md in this directory for context and usage.
"""

import argparse
import asyncio
import json
from pathlib import Path

from jg.coop.lib import mutations
from jg.coop.sync.jobs_scraped.pipelines.llm_opinion import process


GOLD_SET_PATH = Path(__file__).parent / "gold_set.jsonl"


def load_gold_set() -> list[dict]:
    with GOLD_SET_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


async def predict(posting: dict) -> dict:
    item = {"title": posting["title"], "description_text": posting["text"]}
    opinion = (await process(item))["llm_opinion"]
    return {
        "id": posting["id"],
        "keep": posting["keep"],
        "predicted": opinion["is_relevant"],
        "llm_reason": opinion["reason"],
    }


def confusion_matrix(results: list[dict]) -> dict:
    tp = sum(1 for r in results if r["keep"] and r["predicted"])
    fp = sum(1 for r in results if not r["keep"] and r["predicted"])
    fn = sum(1 for r in results if r["keep"] and not r["predicted"])
    tn = sum(1 for r in results if not r["keep"] and not r["predicted"])
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def print_report(results: list[dict], gold_set: dict[str, dict]) -> None:
    print(f"\n{'id':<8} {'gold':<6} {'pred':<6} {'match':<6} reason")
    print("-" * 100)
    for r in sorted(results, key=lambda r: r["id"]):
        match = "OK" if r["keep"] == r["predicted"] else "MISMATCH"
        gold_reason = gold_set[r["id"]]["reason"]
        print(f"{r['id']:<8} {r['keep']!s:<6} {r['predicted']!s:<6} {match:<8}")
        if match == "MISMATCH":
            print(f"         gold reason: {gold_reason}")
            print(f"         llm reason:  {r['llm_reason']}")

    cm = confusion_matrix(results)
    precision = (
        cm["tp"] / (cm["tp"] + cm["fp"]) if (cm["tp"] + cm["fp"]) else float("nan")
    )
    recall = cm["tp"] / (cm["tp"] + cm["fn"]) if (cm["tp"] + cm["fn"]) else float("nan")
    f1_denominator = 2 * cm["tp"] + cm["fp"] + cm["fn"]
    f1 = 2 * cm["tp"] / f1_denominator if f1_denominator else float("nan")
    accuracy = (cm["tp"] + cm["tn"]) / len(results) if results else float("nan")

    print("\nConfusion matrix (gold rows x predicted columns):")
    print(f"  TP (keep/keep):  {cm['tp']}")
    print(f"  FP (drop/keep):  {cm['fp']}")
    print(f"  FN (keep/drop):  {cm['fn']}")
    print(f"  TN (drop/drop):  {cm['tn']}")
    print(f"\nPrecision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1:        {f1:.2%}")
    print(f"Accuracy:  {accuracy:.2%}  ({len(results)} postings)")


def print_diff(results: list[dict], baseline: list[dict]) -> None:
    result_ids = {r["id"] for r in results}
    baseline_ids = {r["id"] for r in baseline}
    if result_ids != baseline_ids:
        raise ValueError(
            "Baseline covers a different set of postings than this run "
            f"(only in baseline: {sorted(baseline_ids - result_ids)}, "
            f"only in this run: {sorted(result_ids - baseline_ids)}); "
            "not comparable."
        )

    baseline_by_id = {r["id"]: r for r in baseline}
    flips = [
        (r, baseline_by_id[r["id"]])
        for r in results
        if r["predicted"] != baseline_by_id[r["id"]]["predicted"]
    ]
    print(f"\n{len(flips)} postings flipped decision vs baseline:")
    for r, old in flips:
        print(f"  {r['id']}: {old['predicted']} -> {r['predicted']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--save", type=Path, help="Save this run's predictions as JSON to this path"
    )
    parser.add_argument(
        "--compare",
        type=Path,
        help="Diff this run's predictions against a previously --save'd JSON file",
    )
    args = parser.parse_args()

    # A stale "already configured" state can survive from an interrupted
    # previous run, since mutations are tracked in the on-disk cache.
    mutations.allow_none()
    mutations.allow("openai")
    try:
        gold_set = load_gold_set()
        gold_set_by_id = {posting["id"]: posting for posting in gold_set}

        async def predict_all():
            return await asyncio.gather(*(predict(posting) for posting in gold_set))

        results = asyncio.run(predict_all())

        print_report(results, gold_set_by_id)

        if args.compare:
            baseline = json.loads(args.compare.read_text(encoding="utf-8"))
            print_diff(results, baseline)

        if args.save:
            args.save.write_text(json.dumps(results, indent=2), encoding="utf-8")
            print(f"\nSaved predictions to {args.save}")
    finally:
        mutations.allow_none()


if __name__ == "__main__":
    main()
