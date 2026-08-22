# CircleCI Guidelines

CI runs on **CircleCI** (`.circleci/config.yml`). When asked to "check CI", "check the build", or "check nightly", diagnose the failure and report analysis + suggested fixes. Do not open a PR until told.

Workflows include the scheduled `nightly` (cron `0 4 * * *` on `main`) and per-branch/PR builds. The approach below works for any of them.

## Accessing the build

The repo is public, so the **CircleCI API needs no token**. Slug is `gh/juniorguru/junior.guru`. Walk down:

1. Latest pipelines: `GET https://circleci.com/api/v2/project/gh/juniorguru/junior.guru/pipeline?branch={branch}` → find pipeline by `number` (nightly runs are the `04:xx` ones on `main`; `02:xx` is `nightly-tidy`).
2. Workflows: `GET /api/v2/pipeline/{pipeline_id}/workflow` → the workflow and its `status`.
3. Jobs: `GET /api/v2/workflow/{workflow_id}/job` → find the failed job and its `job_number`.
4. Step logs: `GET /api/v1.1/project/gh/juniorguru/junior.guru/{job_number}` → each step's `actions[].output_url` is a plain URL you fetch for the log. (v1.1 gives per-step output; v2 does not.)

## Is the failure intermittent?

Always weigh whether the failure is a real regression or a flake — especially for network-heavy jobs like `check-links`, where transient `5xx` are common. Collect the **last ~5 runs of the same workflow**: page through the pipeline list following each response's `next_page_token`, skipping unrelated pipelines on intervening pages (a single page rarely holds 5 nightly runs, since `02:xx` and branch/PR pipelines are interleaved), until 5 matching pipelines are gathered. Then repeat steps 2–4 per pipeline and compare the failed job. Likely intermittent when:

- The same job passed on other recent runs, and/or
- The failing detail differs run to run (e.g. a different URL each time), and/or
- Errors are transient `5xx` / network, not deterministic (`404`, assertion, non-zero from real logic).

A real regression fails the **same way every run** on the same commit range.

When intermittent and the flaky call lives in our own code (a sync request, an API call), the fix is often to retry that request with `tenacity` (already a dependency; see existing usage under `src/jg/coop/sync`) rather than to touch the failing target. External link-check flakes (`check-links`) are handled in lychee config instead.

## Reporting

Give: which job failed, the concrete error, the intermittent-vs-regression verdict with evidence, then suggested fixes. Wait for the user to decide before sending a PR.
