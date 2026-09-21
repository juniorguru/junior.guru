# `llm_opinion` relevance eval

Offline eval for the `is_relevant` decision made by
[`llm_opinion.py`](../../../src/jg/coop/sync/jobs_scraped/pipelines/llm_opinion.py).
Its whole point is to let a prompt change be judged by precision/recall on a
labeled gold set *before* it ships, instead of by watching the live board.

See [issue #1748](https://github.com/juniorguru/junior.guru/issues/1748) for
the background and [issue #1749](https://github.com/juniorguru/junior.guru/issues/1749)
for the prompt change this eval exists to gate.

## Files

- `gold_set.jsonl` — 83 real postings (startupjobs.cz + jobs.cz, scraped
  2026-09-20), each hand-labeled `keep` (true/false) with a one-line `reason`.
  Sampled from a 313-posting pool, weighted towards borderline cases: AI
  coding agents / vibecoding, "build AI" roles, AI-as-a-user-only roles, and
  plain positive/negative controls. See `reason` for what drove each label —
  spot-check any you doubt before trusting the eval blindly.
- `run_eval.py` — calls the real `llm_opinion.process()` (i.e. today's actual
  prompt) over the gold set, prints a per-item table plus a confusion matrix
  with precision/recall/F1, and can diff two runs against each other.
- `baseline_2026-09-21.json` — `run_eval.py --save` output captured against
  the prompt as of 2026-09-21, i.e. *before* the AI-aware rewrite in #1749.
  Precision 38.5% / recall 71.4% / F1 50.0% / accuracy 88.0% (83 postings).
  False positives skew towards AI-adjacent marketing/BI/PPC roles with no
  real code; false negatives skew towards genuine coding-agent roles (e.g.
  a platform engineer using coding agents daily, a plain .NET dev) — exactly
  the failure modes #1749 is meant to fix. Use `--compare` against this file
  to see what a prompt change actually flips.

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

The `--compare` output lists every posting whose `is_relevant` decision
flipped between the two runs, so a prompt change can be eyeballed instead of
just trusted on aggregate precision/recall.
