---
name: code
description: Implement or modify Python, JavaScript, SCSS, templates, CLI, HTTP, logging, or tests in the junior.guru repository. Use for code changes in this project; applies architecture, style, testing, and verification conventions.
---

# Code in junior.guru

## Design and style

- Aim for [Clean Architecture](https://www.youtube.com/watch?v=DJtef410XaM) ([textual slides](https://rhodesmill.org/brandon/slides/2014-07-pyohio/clean-architecture/)): imperative shell wrapping functional core.
- Use Python type hints everywhere.
- Keep cyclomatic complexity low.
- Order module functions from highest-level entry points to progressively smaller helpers. Exception: functions that must exist earlier because module import uses them.
- Use `httpx2` for HTTP requests. Do not add direct use of `requests` or plain `httpx`; those remain transitive dependencies.
- Use `click` for CLI definitions.
- Modern Python and walrus operators are welcome. Follow Ruff `UP` rules.
- Keep Ruff target version compatible with `requires-python`.
- In `key=` callbacks such as `sorted()`, `max()`, and `min()`, prefer `attrgetter` or `itemgetter` over lambda when applicable.
- Do not use `if TYPE_CHECKING:` blocks. Prefer direct imports and annotations.
- Do not place imports inside functions or methods. Keep them at module level.
- In SCSS, prefer `$spacer` over equivalent `map.get($spacers, 3)`.

## Tests

- Develop using red-green TDD.
- Favor many fast unit tests for functional core and few integration tests for imperative shell.
- Tests must not depend on network, current time, or similar external state. Networked smoke/e2e tests must not run by default.
- For remote HTML, download representative pages as fixtures under tests and test against those fixtures. Add multiple fixtures for meaningful edge cases.
- Aim for one descriptive assertion per test function unless impractical, such as checking several small parts of one complex structure.
- Use `@pytest.mark.parametrize` when applicable. Include spaces after commas in parameter names, for example `"secondary_school, university, expected"`.

## Logging

- Set `LOG_LEVEL=debug` to show DEBUG logs. Default level is INFO; selected muted loggers default to WARNING. Configuration lives in `loggers.py`.
- Log potentially sensitive diagnostic details only at DEBUG because CI normally logs INFO.
- Never log actual secrets or other data unsafe for CI output. CI may temporarily enable DEBUG while diagnosing failures that cannot be reproduced locally.

## Verification

- After any code changes, run `uv run jg tidy --code` before finishing.
- Run `uv run jg test` only after substantial Python or JavaScript changes.
- After major SCSS or JavaScript changes, consider `uv run jg web build-static` to catch asset build failures.
- After template, `context.py`, or related rendering changes, consider `uv run jg web build` to verify site generation.

## Sync safety

Never run `uv run jg sync ...` without asking user first. When authorized and necessary, use `uv run jg sync --no-deps ...` to avoid triggering full dependency pipeline.
