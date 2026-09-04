---
name: circleci
description: Diagnose CircleCI failures for a branch, PR, and scheduled nightly builds. Use when asked to check CI, a build, or nightly; report evidence and suggested fixes without opening a PR.
---

# CircleCI Diagnostics

CI runs from `.circleci/config.yml`. Diagnose failures and report analysis plus suggested fixes. Do not open a PR unless explicitly told.

Workflows include per-branch and PR builds, plus scheduled `nightly` on `main` at `0 4 * * *` UTC.

## Access builds

Repository public; CircleCI API needs no token. Project slug: `gh/juniorguru/junior.guru`.

1. List pipelines with `GET https://circleci.com/api/v2/project/gh/juniorguru/junior.guru/pipeline?branch={branch}`. Find target by pipeline `number`. On `main`, `nightly` runs around `04:xx`; `nightly-tidy` runs around `02:xx`.
2. Get workflows with `GET /api/v2/pipeline/{pipeline_id}/workflow` and inspect each workflow's `status`.
3. Get jobs with `GET /api/v2/workflow/{workflow_id}/job`; identify failed job and its `job_number`.
4. Get per-step logs with `GET /api/v1.1/project/gh/juniorguru/junior.guru/{job_number}`. Fetch plain URLs found in `steps[].actions[].output_url`. API v2 does not expose per-step output.

## Distinguish regression from flake

Always compare roughly five recent runs of same workflow, especially for network-heavy jobs such as `check-links`.

Follow pipeline response `next_page_token` across pages until five matching pipelines are collected. Skip unrelated PR, branch, `nightly`, or `nightly-tidy` pipelines interleaved in results. For every matching pipeline, inspect workflows, jobs, and relevant step logs as above.

Evidence favors intermittent failure when:

- Same job passes in other recent runs.
- Failure detail changes between runs, such as different URLs.
- Errors are transient network failures or `5xx` responses.

Evidence favors regression when same deterministic error repeats across runs in same commit range, such as `404`, assertion failure, or non-zero exit from application logic.

When flaky call belongs to project code, retrying with `tenacity` is often appropriate; dependency already used under `src/jg/coop/sync`. Handle external `check-links` flakes in lychee configuration instead of changing remote target.

## Report

Include:

- Failed job.
- Concrete error from logs.
- Intermittent-versus-regression verdict with evidence from recent comparable runs.
- Suggested fixes.

Wait for user decision before opening PR or implementing fixes unless implementation was explicitly requested.
