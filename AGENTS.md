# Local Run Guide (junior.guru)

## Quick start (minimal website only)
- Python deps: `uv sync` (creates `.venv`).
- Node deps: `npm install`.
- Build: `./.venv/bin/jg web build`.
- Serve (build + live reload): `./.venv/bin/jg web serve`.
- Default URL: `http://localhost:5500/`.
- Build output: `public/`.

## Node toolchain note
In this environment, the `node` shim crashed. Using an explicit Node in PATH worked:
`PATH=/Users/satan/.proto/tools/node/22.21.1/bin:$PATH <command>`.
If `npm/npx` or `jg web build/serve` fail because of Node, try the same approach.

## Data + strict build requirements
The web build runs in strict mode. Missing data can cause template failures.
Important paths:
- SQLite DB: `src/jg/coop/data/data.db` (gitignored).
- Jobs API source files (required by post-build):
  - `src/jg/coop/data/jobs/jobs.jsonl`
  - `src/jg/coop/data/jobs/schema-apify.json`
  Empty stub files are fine to avoid build errors.

Common DB-related failures and what they imply:
- Handbook pages reference specific event IDs: 18, 36, 45.
- Event pages sample from planned + archive lists; keep at least 2 planned and 3 archived events to avoid empty samples.
- `handbook/cv.md` references podcast episode #1.
- `.nav.yml` expects `news/*.md`; at least 1 newsletter issue must exist or MkDocs will fail in strict mode.
- Topic docs require topics: `adventofcode`, `javascript`, `python`.
- Course provider pages must exist for slugs referenced in `src/jg/coop/data/redirects.yml` (all `courses/*.md` targets).
- Charts are heavily used in `src/jg/coop/web/docs/about/*.md` and `club.md`; missing chart keys cause template errors. If charts are missing, either sync real data or stub the needed chart slugs/keys.

## Minimal seed script (safe, non-destructive)
Use this only if `data.db` is missing or empty and you want the site to render.
It creates the minimum rows (or skips if they exist).

```bash
./.venv/bin/python scripts/seed_minimal.py
```

After seeding, ensure the jobs API stubs exist:
`mkdir -p src/jg/coop/data/jobs && : > src/jg/coop/data/jobs/jobs.jsonl && printf '{}' > src/jg/coop/data/jobs/schema-apify.json`

## dev-browser validation (optional)
- Start server: `cd /Users/satan/side/experiments/junior.guru/.codex/skills/dev-browser && ./server.sh`
- Run scripts from that directory (see skill docs).

## Extra notes
- The build uses MkDocs strict mode; warnings can fail the build.
- Logging can be enabled with `export LOG_LEVEL=debug` if needed.
