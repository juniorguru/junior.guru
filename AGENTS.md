# AGENTS.md

This file provides guidance to AI coding assistants when working with code in this repository.

## Project Overview

junior.guru is a Czech community platform for junior developers. The codebase includes:
- A website built with MkDocs
- A Discord bot (using py-cord)
- Data synchronization scripts that pull from various external sources
- Image generation for social media thumbnails and posters

## Tech Stack

- **Python 3.13** with uv for package management
- **Node.js 22** with npm for frontend assets
- **Peewee ORM** with SQLite database (`src/jg/coop/data/data.db`)
- **MkDocs** for static site generation
- **esbuild** for JS/CSS bundling with SCSS
- **Bootstrap 5** with custom SCSS
- **CircleCI** for CI/CD

## Common Commands

### Development
```bash
uv sync                     # Install Python dependencies
npm ci                      # Install JS dependencies
playwright install firefox  # Install browser for screenshots
uv run jg web serve         # Build and serve website with live reload
uv run jg web build         # Build website to public/
```

### Testing
```bash
uv run jg test              # Run all tests (Python + JS + SCSS lint)
uv run pytest tests/test_lib_md.py -v  # Run single Python test file
uv run pytest -k "test_name" -v        # Run specific test by name
npx vitest --dir=tests --run           # Run JS tests only
npx stylelint "src/jg/coop/css/**/*.*css"  # Lint SCSS only
```

### Sync Commands
```bash
uv run jg sync <name>       # Run specific sync command (e.g., jobs-listing)
uv run jg sync jobs         # Run all job-related syncs in order
uv run jg sync all          # Run all sync commands
uv run jg sync --no-deps <name>  # Skip dependencies
```

### Code Quality
```bash
uv run jg tidy              # Format all code (Python, JS, Jinja, SCSS) + optimize images
uv run ruff check --fix     # Fix Python linting issues
uv run ruff format          # Format Python code
npx @biomejs/biome format --write  # Format JS code
```

## Local Run Guide

### Quick start (minimal website only)
- Install deps: `uv sync` and `npm ci` (or `npm install`).
- Optional minimal seed (if `data.db` is missing/empty): `./.venv/bin/python scripts/seed_minimal.py`.
- Ensure jobs API stubs exist (required by post-build):
  - `mkdir -p src/jg/coop/data/jobs`
  - `: > src/jg/coop/data/jobs/jobs.jsonl`
  - `printf '{}' > src/jg/coop/data/jobs/schema-apify.json`
- Build: `uv run jg web build` (output in `public/`).
- Serve: `uv run jg web serve` (default: `http://localhost:5500/`).

### Node toolchain note
In this environment, the `node` shim crashed. Using an explicit Node in PATH worked:
`PATH=/Users/satan/.proto/tools/node/22.21.1/bin:$PATH <command>`.
If `npm/npx` or `jg web build/serve` fail because of Node, try the same approach.

### Strict build and data requirements
MkDocs runs in strict mode; warnings and missing data can break builds.

- DB location: `src/jg/coop/data/data.db` (gitignored).
- Event pages sample from planned + archive lists; keep at least 2 planned and 3 archived events.
- Handbook pages reference specific event IDs: 18, 36, 45.
- `handbook/cv.md` references podcast episode #1.
- `.nav.yml` expects `news/*.md`; at least 1 newsletter issue must exist.
- Topic docs require topics: `adventofcode`, `javascript`, `python`.
- Course provider pages must exist for slugs referenced in `src/jg/coop/data/redirects.yml` (all `courses/*.md` targets).
- Charts are heavily used in `src/jg/coop/web/docs/about/*.md` and `club.md`; missing chart keys cause template errors. If charts are missing, either sync real data or stub the needed chart slugs/keys.

### dev-browser validation (optional)
- Start server: `cd /Users/satan/side/experiments/junior.guru/.codex/skills/dev-browser && ./server.sh`
- Run scripts from that directory (see skill docs).

## Architecture

### Package Structure (`src/jg/coop/`)
- `cli/` - Click CLI commands (entry point: `jg` or `coop`)
- `lib/` - Shared utility modules (caching, Discord helpers, image processing, etc.)
- `models/` - Peewee database models
- `sync/` - Data synchronization modules that populate the database
- `web/` - MkDocs site (docs/, theme/, macros/, generators.py)
- `data/` - SQLite database, JSONL files, YAML configs
- `images/` - Static images and generated assets
- `css/` - SCSS stylesheets
- `js/` - JavaScript modules

### Sync System
The sync system uses a dependency-based execution model:

```python
from jg.coop.cli.sync import main as cli

@cli.sync_command(dependencies=["jobs-scraped", "jobs-submitted"])
@db.connection_context()
def main():
    # Sync logic here
```

- Sync commands are discovered automatically from `sync/` package
- Dependencies are resolved via topological sort
- Use `@db.connection_context()` for database operations
- The `--allow-mutations` flag controls external API writes

### Database
- SQLite with WAL mode at `src/jg/coop/data/data.db`
- Models extend `BaseModel` from `models/base.py`
- Use `db.connection_context()` decorator for database access
- Czech sorting supported via `czech_sort` SQL function

### Web (MkDocs)
- Config at `src/jg/coop/web/mkdocs.yml`
- Jinja templates in `web/theme/`
- Custom macros in `web/macros/`
- Page generators in `web/generators.py`
- Generated docs output to `web/generated_docs/`

## Key Patterns

### Logging
```python
from jg.coop.lib import loggers
logger = loggers.from_path(__file__)
logger.info("Message")
logger["sublogger"].debug("Detailed message")
```
Set `LOG_LEVEL=debug` for verbose output.

### Caching
```python
from jg.coop.lib.cache import cache
from datetime import timedelta

@cache(expire=timedelta(hours=6), tag="my-cache")
def expensive_operation():
    ...
```

### External Integrations
The codebase integrates with: Discord (py-cord), Apify (web scraping), Stripe, Memberful, Google Sheets, GitHub, Mastodon, Buttondown (newsletter), Fakturoid (invoicing).

## Linting Configuration
- **Python**: ruff (see `pyproject.toml`)
- **JavaScript**: Biome (see `biome.json`)
- **SCSS**: Stylelint with Bootstrap config

## Notes
- Sensitive data goes to DEBUG logs only (CI logs INFO level)
- The `*_legacy` directories are excluded from linting
- Tests use pytest with ruff integration (`--ruff --ruff-format` flags)
