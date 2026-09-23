"""Offline precision/recall eval for llm_opinion.process(), built on pydantic-evals.

See README.md in this directory for context and usage.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path

from pydantic_evals import Dataset
from pydantic_evals.evaluators import EqualsExpected
from pydantic_evals.evaluators.report_common import ConfusionMatrixEvaluator
from pydantic_evals.evaluators.report_evaluator import (
    ReportEvaluator,
    ReportEvaluatorContext,
)
from pydantic_evals.reporting import EvaluationReport, EvaluationReportAdapter
from pydantic_evals.reporting.analyses import ScalarResult

from jg.coop.lib import mutations
from jg.coop.sync.jobs_scraped.pipelines.llm_opinion import process


GOLD_SET_PATH = Path(__file__).parent / "gold_set.yaml"

# Populated as a side effect of relevance_task(), keyed by case id, so mismatches can
# show the LLM's reasoning without changing the task's output type: it stays a plain
# bool, which is what EqualsExpected/ConfusionMatrixEvaluator compare out of the box.
llm_reasons: dict[str, str] = {}


async def relevance_task(inputs: dict) -> bool:
    item = {"title": inputs["title"], "description_text": inputs["text"]}
    opinion = (await process(item))["llm_opinion"]
    llm_reasons[inputs["id"]] = opinion["reason"]
    return opinion["is_relevant"]


@dataclass(repr=False)
class PrecisionRecallF1(ReportEvaluator):
    """Scalar precision/recall/F1 for the boolean is_relevant decision.

    pydantic-evals ships PrecisionRecallEvaluator, but that's a threshold curve
    over continuous scores; is_relevant is already a hard boolean, so a plain
    confusion-matrix-derived scalar is more direct.
    """

    def evaluate(self, ctx: ReportEvaluatorContext) -> list[ScalarResult]:
        tp = fp = fn = 0
        for case in ctx.report.cases:
            if case.output and case.expected_output:
                tp += 1
            elif case.output and not case.expected_output:
                fp += 1
            elif not case.output and case.expected_output:
                fn += 1
        precision = 100 * tp / (tp + fp) if (tp + fp) else float("nan")
        recall = 100 * tp / (tp + fn) if (tp + fn) else float("nan")
        f1_denominator = 2 * tp + fp + fn
        f1 = 100 * 2 * tp / f1_denominator if f1_denominator else float("nan")
        return [
            ScalarResult(title="Precision", value=round(precision, 1), unit="%"),
            ScalarResult(title="Recall", value=round(recall, 1), unit="%"),
            ScalarResult(title="F1", value=round(f1, 1), unit="%"),
        ]


def load_dataset() -> Dataset[dict, bool, dict]:
    loaded = Dataset[dict, bool, dict].from_file(GOLD_SET_PATH)
    return Dataset[dict, bool, dict](
        name=loaded.name,
        cases=loaded.cases,
        evaluators=[EqualsExpected()],
        report_evaluators=[ConfusionMatrixEvaluator(), PrecisionRecallF1()],
    )


def print_mismatches(report: EvaluationReport) -> None:
    mismatches = [case for case in report.cases if case.output != case.expected_output]
    print(f"\n{len(mismatches)} mismatches:")
    for case in sorted(mismatches, key=lambda c: c.name):
        print(f"\n  {case.name} (gold={case.expected_output}, predicted={case.output})")
        print(f"    gold reason: {case.metadata['gold_reason']}")
        print(f"    llm reason:  {llm_reasons.get(case.name, '?')}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", type=Path, help="Save this run's report as JSON")
    parser.add_argument(
        "--compare",
        type=Path,
        help="Render this run against a previously --save'd report",
    )
    args = parser.parse_args()

    # A stale "already configured" state can survive from an interrupted
    # previous run, since mutations are tracked in the on-disk cache.
    mutations.allow_none()
    mutations.allow("openai")
    try:
        dataset = load_dataset()
        report = dataset.evaluate_sync(relevance_task)
        if report.failures:
            failed = ", ".join(failure.name for failure in report.failures)
            raise RuntimeError(f"Task execution failed for: {failed}")

        baseline = None
        if args.compare:
            baseline = EvaluationReportAdapter.validate_json(args.compare.read_bytes())

        report.print(baseline=baseline, include_averages=True)
        print_mismatches(report)

        if args.save:
            args.save.write_bytes(EvaluationReportAdapter.dump_json(report, indent=2))
            print(f"\nSaved report to {args.save}")
    finally:
        mutations.allow_none()


if __name__ == "__main__":
    main()
