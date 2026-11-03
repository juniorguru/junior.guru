---
name: circleci
description: Diagnose CircleCI failures for a branch, PR, and scheduled nightly builds. Use when asked to check CI, a build, or nightly; report evidence and suggested fixes without opening a PR.
---

# CircleCI Diagnostics

CI runs from `.circleci/config.yml`. Diagnose failures and report analysis plus suggested fixes. Do not open a PR unless explicitly told.

Workflows include per-branch and PR builds, plus scheduled `nightly` on `main` at `0 4 * * *` UTC.

## Access builds

Repository public; CircleCI API needs no token. Use API v3 (`https://circleci.com/api/v3`). Project ID: `ecf683af-646e-4014-8483-a95ab98fa816`. Pages have max 20 items; follow `page.next` as `page[cursor]`. Use `curl -g`.

1. List runs with `GET /api/v3/runs?filter[project_id]={project_id}&page[limit]=20`. There is no branch filter: check `references.event.attributes.vcs.branch` and `references.trigger.attributes.event_source.type` (`schedule` for scheduled). On `main`, `nightly` runs around `04:xx`; `nightly-tidy` runs around `02:xx`.
2. Get workflows with `GET /api/v3/workflows?filter[run_id]={run_id}` and inspect each workflow's `attributes.phase` and `attributes.outcome`.
3. Get jobs with `GET /api/v3/jobs?filter[workflow_id]={workflow_id}`; identify failed job and its `attributes.number` (job number).
4. Get per-step logs with `GET /api/v1.1/project/gh/juniorguru/junior.guru/{job_number}`. Fetch plain URLs found in `steps[].actions[].output_url`. API v3 job details and logs require a token, so use v1.1 for them.

## Distinguish regression from flake

Always compare roughly five recent runs of same workflow, especially for network-heavy jobs such as `check-links`.

Follow runs `page.next` across pages until five matching runs are collected. Skip unrelated PR, branch, `nightly`, or `nightly-tidy` runs interleaved in results. For every matching run, inspect workflows, jobs, and relevant step logs as above.

Evidence favors intermittent failure when:

- Same job passes in other recent runs.
- Failure detail changes between runs, such as different URLs.
- Errors are transient network failures or `5xx` responses.

Evidence favors regression when same deterministic error repeats across runs in same commit range, such as `404`, assertion failure, or non-zero exit from application logic.

When flaky call belongs to project code, retrying with `tenacity` is often appropriate; dependency already used under `src/jg/coop/sync`. Handle external `check-links` flakes in lychee configuration instead of changing remote target.

## Reminders

Some nightly failures are intentional reminders for the maintainer, not breakages. Report them as reminders, not as regressions or flakes:

- `check-sponsors` failing with `renews soon!` errors, as a sponsor's renewal date approaches. Fails nightly until the sponsorship gets renewed or ended and `src/jg/coop/data/sponsors.yml` updated.

## Report

Include:

- Failed job.
- Concrete error from logs.
- Intermittent-versus-regression verdict with evidence from recent comparable runs.
- Suggested fixes.

Wait for user decision before opening PR or implementing fixes unless implementation was explicitly requested.
