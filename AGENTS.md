# Guidance for AI agents

- The only allowed stylizations of the project name in regular sentences or headings are "junior.guru" and "Junior Guru".
- Always run the `jg` project CLI as `uv run jg`. Always prefer `uv` over custom Python binary and virtual environment management.
- After any changes inside `src/jg/coop/images`, always run `uv run jg tidy` before finishing the work.
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
