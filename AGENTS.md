# Guidance for AI agents

- The only allowed stylizations of the project name in regular sentences or headings are "junior.guru" and "Junior Guru".
- Always run the `jg` project CLI as `uv run jg`. Always prefer `uv` over custom Python binary and virtual environment management.
- Treat `jg sync` as a danger area. Never execute it deliberately unless the user explicitly instructed or approved that exact sync operation.
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
