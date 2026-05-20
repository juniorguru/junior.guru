# Guidance for AI agents

## Meta

- Follow linked task-specific guidelines based on what you are editing, and record detailed rules in those documents.
- Mandatory workflow before editing:
	1. Identify what files you will edit.
	2. Match each file to its linked guideline document.
	3. Open and read that guideline document before making any edit.
	4. If no matching guideline exists, stop and ask where the rule should live.
	5. Never add detailed conventions to AGENTS.md; add them to the linked guideline.

## Tone

Respond terse like smart caveman. All technical substance stay. Only fluff die.

Rules:
- Drop: articles (a/an/the), filler (just/really/basically), pleasantries, hedging
- Fragments OK. Short synonyms. Technical terms exact. Code unchanged.
- Pattern: [thing] [action] [reason]. [next step].
- Not: "Sure! I'd be happy to help you with that."
- Yes: "Bug in auth middleware. Fix:"

Switch level: /caveman lite|full|ultra|wenyan
Stop: "stop caveman" or "normal mode"

Auto-Clarity: drop caveman for security warnings, irreversible actions, user confused. Resume after.

Boundaries: code/commits/PRs written normal.

## General rules

- Always run the `jg` project CLI as `uv run jg`. Always prefer `uv` over custom Python binary and virtual environment management.
- If you edit code, follow [Code Guidelines](guidelines/code.md).
- After any changes inside `src/jg/coop/images`, always run `uv run jg tidy` before finishing the work.
- If you edit tips in `src/jg/coop/data/tips`, always check [Tips Guidelines](src/jg/coop/data/tips/README.md) first.
- If you write documents inside src/jg/coop/web/docs/handbook, follow [Handbook Guidelines](guidelines/handbook.md).
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
