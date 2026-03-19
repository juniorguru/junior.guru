# AGENTS

- In pytest `@pytest.mark.parametrize`, always include spaces after commas in the argument list, e.g. "secondary_school, university, expected".
- Do not use `if TYPE_CHECKING:` blocks. Prefer straightforward imports/annotations without this pattern.
- Do not use inline imports inside functions or methods. Keep imports at module level.
- After changes to code or images, always run `uv run jg tidy --code` before finishing the work.
- Run `uv run jg test` only if you made substantial changes to Python or JavaScript code.
- After major SCSS or JavaScript edits, consider running `uv run jg web build-static` to catch asset build issues.
- After changes to templates, `context.py`, or related web rendering logic, consider running `uv run jg web build` to verify site generation.
- Never run `uv run jg sync ...` yourself without asking. If you must, run `uv run jg sync --no-deps ...` so you don't accidentally run the whole pipeline of depending sync scripts.
