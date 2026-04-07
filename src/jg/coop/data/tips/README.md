# Tips

Tips are short guidance texts for club members. The `jg sync tips` script loads them, parses them, and syncs them to Discord as separate forum threads.

This document is a practical style guide: what to keep consistent in content, language, and technical format so tips keep one voice and pass the parser.

## Voice and tone

- Perspective: tips are written from the point of view of the kuře bot.
- Bot self-reference: kuře uses first person and Czech neuter gender (for example: "pomohlo jsem").
- Honza: refer to Honza in third person (typically `<@HONZA>`), not as "I".
- Audience: address the reader directly in second person singular (for example: "můžeš", "zkus", "napiš").
- Style: friendly, supportive, informal, but still factual; no lecturing and no belittling beginners.
- Community framing: emphasize safety, collaboration, and practical orientation in the club.

## Tip structure

- One file = one tip.
- A tip starts with an H1 heading in the format `# {emoji} {title}`. The emoji must be unique within the set of H1s from all the other tips.
- After H1, include a short opening paragraph (lead).
- Then usually add multiple `##` sections with clear subtitles, always followed by a suitable emoji. These emojis must be unique within the set of H2s of that particular tip file.
- Sections often end with a concrete call to action (where to post, what to click, what to set up).

## Language conventions

- Tips themselves are written in Czech, using plain vocabulary and short to medium paragraphs.
- Practical examples are encouraged (what exactly to do, where to find it).
- Links should point directly to relevant sources (handbook, help docs, Discord thread, etc.).

## Discord reference conventions

The parser can resolve symbolic references to Discord IDs. Use these forms:

- Channels: `<#INTRO>`, `<#CHAT>`, `<#ANNOUNCEMENTS>`
- Users: `<@HONZA>`, `<@LUCIE>`
- Roles: `<@&MOST_HELPFUL>`, `<@&EVENTS_ORGANIZER>`

Notes:

- Values inside the brackets must match constants/slugs known by the system.
- Write abbreviations consistently in uppercase, following existing tips.

Where to find the system-known values:

- Channels (`<#...>`) are defined in `ClubChannelID` in [src/jg/coop/lib/discord_club.py](../../../lib/discord_club.py).
- Users (`<@...>`) are defined in `ClubMemberID` in [src/jg/coop/lib/discord_club.py](../../../lib/discord_club.py).
- Role slugs used in tips (`<@&...>`) come from `registry[].slug` in [src/jg/coop/data/roles.yml](../roles.yml).

## Parser technical requirements

These points are important because `jg sync tips` requires them:

- The file must be `.md` inside `src/jg/coop/data/tips`.
- `README.md` is ignored; other `.md` files are loaded.
- Filename format: `{order}_{slug}.md` (for example `01_bot.md`, `12_feedback.md`).
- `order` is a text-based ordering key used for sorting; keep a two-digit format (`01`, `02`, ...).
- The first line must be an H1 (`# ...`), otherwise parsing fails.
- The H1 must start with an emoji; that emoji is used as the tip identity during sync.
- The first non-empty line after H1 is used as the lead (short description).

## Maintenance recommendations

- Edit existing tips in a way that preserves voice and formatting consistency.
- Before adding a new tip, check whether the topic is already covered.
- Keep new tips similar in length to existing ones (brief but actionable).
