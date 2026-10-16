# Guidance for AI agents

- The only allowed stylizations of the project name in regular sentences or headings are "junior.guru" and "Junior Guru".
- Always run the `jg` project CLI as `uv run jg`. Always prefer `uv` over custom Python binary and virtual environment management.
- Write GitHub issues, PRs, and comments in English, even when the source material (e.g. a quoted message) is in Czech.
- When working locally under close supervision, never commit until the user says so, and leave changes uncommitted for them to review. However, if a session (especially a claude.ai/code cloud session) starts with a request to open or create a pull request, take that as permission to handle git yourself: branch, commit, push, and open the PR.
- When addressing review comments on a GitHub pull request, resolve each thread you believe your changes have addressed. If you want to discuss an approach or decline a suggestion, reply in that comment thread on GitHub.
- Don't subscribe to pull request events unless the user asks for it.
- Treat `jg sync` as a danger area. Never execute it deliberately unless the user explicitly instructed or approved that exact sync operation.
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
- The package imported as `discord` is [Pycord](https://docs.pycord.dev), not discord.py — the two differ, and Pycord is often installed bleeding-edge from git. Never rely on discord.py knowledge; always read the installed package source under `.venv/lib/**/site-packages/discord/` before drawing conclusions about its behavior.
- In Czech text, use a non-breaking space (the U+00A0 character directly, not the `&nbsp;` entity) where Czech typography forbids a line break, following the [ÚJČ rules](https://prirucka.ujc.cas.cz/?id=880): after the one-letter words k, s, v, z, o, u, a, i, in numbers and between a number and its unit, after "tj.", "tzv.", "tzn.", and similar. After editing any Markdown, Jinja, or HTML under `src/jg/coop/web`, run `uv run jg tidy fix-nbsp` before committing, which adds the missing ones automatically. Elsewhere (e.g. Czech strings in Python code), add them by hand.
