---
name: tips
description: Create or edit Czech club-member tips in src/jg/coop/data/tips for Discord synchronization. Use for tip content, filenames, headings, emoji identity, symbolic Discord references, voice, or parser compatibility.
---

# Club Tips

Tips are short guidance texts for club members. `jg sync tips` parses them and synchronizes each tip to Discord as a separate forum thread.

## Voice and language

- Write from perspective of kuře bot.
- Kuře refers to itself in first person using Czech neuter gender, for example `pomohlo jsem`.
- Refer to Honza in third person, typically as `<@HONZA>`, never as bot's `já`.
- Address reader directly in second-person singular: `můžeš`, `zkus`, `napiš`.
- Use friendly, supportive, informal, factual Czech. Never lecture or belittle beginners.
- Emphasize community safety, collaboration, and practical orientation.
- Prefer plain vocabulary, short-to-medium paragraphs, concrete steps, and direct links to relevant sources.

## Structure

- One Markdown file represents one tip.
- Filename format: `{order}_{slug}.md`, for example `01_bot.md` or `12_feedback.md`.
- Keep `order` as two-digit text sorting key: `01`, `02`, and so on.
- First line must be `# {emoji} {title}`. Parser uses H1 emoji as tip identity; it must be unique across all tip H1s.
- First non-empty line after H1 becomes lead. Keep it short.
- Usually add several `## {subtitle} {emoji}` sections. Each H2 emoji must be unique within that file.
- Sections often end with concrete call to action: where to post, what to click, or what to configure.
- Before adding tip, check whether existing tip covers topic. Match existing tips' brief, actionable length.

Only `.md` files directly under `src/jg/coop/data/tips` are loaded. `README.md` was historically ignored by parser and is no longer used for guidance.

## Discord references

Parser resolves symbolic Discord references:

- Channels: `<#INTRO>`, `<#CHAT>`, `<#ANNOUNCEMENTS>`
- Users: `<@HONZA>`, `<@LUCIE>`
- Roles: `<@&MOST_HELPFUL>`, `<@&EVENTS_ORGANIZER>`

Bracketed names must match system-known constants or slugs. Keep abbreviations uppercase and consistent with existing tips.

- Channel names come from `ClubChannelID` in `src/jg/coop/lib/discord_club.py`.
- User names come from `ClubMemberID` in `src/jg/coop/lib/discord_club.py`.
- Role names come from `registry[].slug` in `src/jg/coop/data/roles.yml`.

## Preserve compatibility

When editing existing tips, preserve voice, heading format, unique emoji identities, valid symbolic references, and filename ordering. Parser fails when first line is not H1 or H1 does not begin with emoji.
