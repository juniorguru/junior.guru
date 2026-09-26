# `llm_opinion` relevance eval

Offline eval for the `is_relevant` decision made by
[`llm_opinion.py`](../../../src/jg/coop/sync/jobs_scraped/pipelines/llm_opinion.py).
Its whole point is to let a prompt change be judged by precision/recall on a
labeled gold set *before* it ships, instead of by watching the live board.

See [issue #1748](https://github.com/juniorguru/junior.guru/issues/1748) for
the background and [issue #1749](https://github.com/juniorguru/junior.guru/issues/1749)
for the prompt change this eval exists to gate.

Built on [pydantic-evals](https://ai.pydantic.dev/evals/): the gold set is a
`pydantic_evals.Dataset` (cases = postings, `expected_output` = the gold
`keep` bool), `run_eval.py` runs it through the real
`llm_opinion.process()` as the task function, and reporting/diffing is the
library's own `EvaluationReport`.

## Files

- `gold_set.yaml` (+ `gold_set_schema.json`, generated alongside it) — 83
  real postings (startupjobs.cz + jobs.cz, scraped 2026-09-20) as a
  `pydantic_evals.Dataset`. Each case's `expected_output` is the hand-labeled
  `keep` (true/false) decision; `metadata.gold_reason` explains why. Sampled
  from a 313-posting pool, weighted towards borderline cases: AI coding
  agents / vibecoding, "build AI" roles, AI-as-a-user-only roles, and plain
  positive/negative controls. Spot-check any `gold_reason` you doubt before
  trusting the eval blindly.
- `run_eval.py` — loads the dataset, wires up `EqualsExpected` (per-case
  pass/fail), the built-in `ConfusionMatrixEvaluator`, and a small custom
  `PrecisionRecallF1` report evaluator, then calls
  `dataset.evaluate_sync(relevance_task)` against the real
  `llm_opinion.process()` (i.e. today's actual prompt). Prints the report
  plus a confusion matrix and precision/recall/F1, and can render a diff
  against a previously `--save`d report.
- `baseline_2026-09-21.json` — an `EvaluationReport` (via
  `EvaluationReportAdapter`) captured against the prompt as of 2026-09-21,
  i.e. *before* the AI-aware rewrite in #1749. Precision 38.5% / recall
  71.4% / F1 50.0% / accuracy 88.0% (83 postings). False positives skew
  towards AI-adjacent marketing/BI/PPC roles with no real code; false
  negatives skew towards genuine coding-agent roles (e.g. a platform
  engineer using coding agents daily, a plain .NET dev) — exactly the
  failure modes #1749 is meant to fix. Use `--compare` against this file to
  see what a prompt change actually flips.

This directory intentionally has no `test_*.py` file, so plain `pytest` never
picks it up — running it costs real OpenAI calls (though `ask_llm` caches
responses for 60 days, so reruns with an unchanged prompt are free).

## Running it

Requires `OPENAI_API_KEY` in the environment.

```sh
uv run python tests/sync_jobs_scraped_pipelines/llm_opinion_eval/run_eval.py
```

To compare against the checked-in baseline after changing the prompt (e.g. for #1749):

```sh
uv run python tests/sync_jobs_scraped_pipelines/llm_opinion_eval/run_eval.py \
  --compare tests/sync_jobs_scraped_pipelines/llm_opinion_eval/baseline_2026-09-21.json \
  --save tests/sync_jobs_scraped_pipelines/llm_opinion_eval/baseline_$(date +%F).json
```

`--save`ing a fresh dated baseline after a shipped prompt change keeps the
comparison point current for the next iteration.

`--compare` renders pydantic-evals' own diff table (per-case assertion
pass/fail side by side) and prints the mismatched cases in full, so a prompt
change can be eyeballed instead of just trusted on aggregate
precision/recall.
