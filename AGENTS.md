# Guidance for AI agents

- The only allowed stylizations of the project name in regular sentences or headings are "junior.guru" and "Junior Guru".
- Always run the `jg` project CLI as `uv run jg`. Always prefer `uv` over custom Python binary and virtual environment management.
- Write GitHub issues, PRs, and comments in English, even when the source material (e.g. a quoted message) is in Czech.
- When working locally under close supervision, never commit until the user says so, and leave changes uncommitted for them to review. However, if a session (especially a claude.ai/code cloud session) starts with a request to open or create a pull request, take that as permission to handle git yourself (see the `pull-requests` skill).
- Treat `jg sync` as a danger area. Never execute it deliberately unless the user explicitly instructed or approved that exact sync operation.
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
- The package imported as `discord` is [Pycord](https://docs.pycord.dev), not discord.py — the two differ, and Pycord is often installed bleeding-edge from git. Never rely on discord.py knowledge; always read the installed package source under `.venv/lib/**/site-packages/discord/` before drawing conclusions about its behavior.
