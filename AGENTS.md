# Guidance for AI agents

- The only allowed stylizations of the project name in regular sentences or headings are "junior.guru" and "Junior Guru".
- In any Python change, keep data transformation in pure, unit-tested functions, separate from I/O (database, HTTP, files, Discord). Details are in the `code` skill (`.claude/skills/code/SKILL.md`). Don't copy mixed patterns from surrounding code.
- Always run the `jg` project CLI as `uv run jg`. Always prefer `uv` over custom Python binary and virtual environment management.
- Write GitHub issues, PRs, and comments in English, even when the source material (e.g. a quoted message) is in Czech.
- When working locally under close supervision, never commit until the user says so, and leave changes uncommitted for them to review. However, if a session (especially a claude.ai/code cloud session) starts with a request to open or create a pull request, take that as permission to handle git yourself: branch, commit, push, and open the PR.
- When addressing review comments on a GitHub pull request, resolve each thread you believe your changes have addressed. If you want to discuss an approach or decline a suggestion, reply in that comment thread on GitHub.
- Don't subscribe to pull request events unless the user asks for it.
- Treat `jg sync` as a danger area. Never execute it deliberately unless the user explicitly instructed or approved that exact sync operation.
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
- The package imported as `discord` is [Pycord](https://docs.pycord.dev), not discord.py — the two differ, and Pycord is often installed bleeding-edge from git. Never rely on discord.py knowledge; always read the installed package source under `.venv/lib/**/site-packages/discord/` before drawing conclusions about its behavior.
- In Czech text (Markdown, templates, and string values in code), put a non-breaking space after one- and two-letter words such as "a", "v", "i", "s", "k", "na", so that a line never ends with them. Use the Unicode character U+00A0 directly, not the `&nbsp;` entity.
- Screenshot files are named after the URL they show (see `screenshot_url()` in `src/jg/coop/lib/template_filters.py`, e.g. `https://www.youtube.com/@RobWebSK` → `youtube-com-robwebsk.webp`). Every time you change the URL of a course provider or a link inside a card, check whether a corresponding screenshot exists in `src/jg/coop/images/screenshots*/` and rename it to fit the new URL.
- The SQLite database is `src/jg/coop/data/data.db` (see `DB_FILE` in `src/jg/coop/models/base.py`). Query it strictly read-only: `sqlite3 "file:src/jg/coop/data/data.db?immutable=1" "..."`. Never point `sqlite3` at a path you haven't checked, as it silently creates an empty database there, and an empty result then looks like missing data.
- When committing, stage explicit paths and check `git status` first. Never use `git add -A` or `git add .`, which sweep in stray files created by accident.
