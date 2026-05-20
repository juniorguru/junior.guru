# Contributing to junior.guru

- Follow linked task-specific guidelines based on what you are editing, and record detailed rules in those documents.
- Mandatory workflow before editing:
	1. Identify what files you will edit.
	2. Match each file to its linked guideline document.
	3. Open and read that guideline document before making any edit.
	4. If no matching guideline exists, stop and ask where the rule should live.
	5. Never add detailed conventions to AGENTS.md; add them to the linked guideline.
- If you edit code, follow [Code Guidelines](guidelines/code.md).
- After any changes inside `src/jg/coop/images`, always run `uv run jg tidy` before finishing the work.
- If you edit tips in `src/jg/coop/data/tips`, always check [Tips Guidelines](src/jg/coop/data/tips/README.md) first.
- If you write documents inside src/jg/coop/web/docs/handbook, follow [Handbook Guidelines](guidelines/handbook.md).
- After significant changes to the Discord integration always check the [bot docs](src/jg/coop/web/docs/about/bot.md) if they need update.
