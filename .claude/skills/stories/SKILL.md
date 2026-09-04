---
name: stories
description: Add or edit junior.guru interview stories and participant photos under src/jg/coop/web/docs/stories and src/jg/coop/images/avatars-participants. Use for importing an interview from Google Docs, formatting story Markdown, or preparing its portrait.
---

# Junior Guru Stories

Stories are Markdown pages in `src/jg/coop/web/docs/stories` within the MkDocs junior.guru website.

## Add a story

Story author Adéla typically provides a Google Docs interview and attaches participant photo.

1. In Google Docs, choose **Download → Markdown (.md)**.
2. Save Markdown under `src/jg/coop/web/docs/stories`. Name file after interviewee: lowercase, no diacritics, whitespace replaced with hyphens.
3. Save photo under `src/jg/coop/images/avatars-participants` using same filename convention.
4. Inspect photo and choose largest aesthetically pleasing square crop. Convert it to JPEG with `.jpg` extension.
5. Inspect existing stories, then adapt imported Markdown to their conventions: front matter, navigation markup, article lead, and interview formatting.
6. Run `uv run jg tidy` to optimize images.

## Formatting

- Separate every question and answer with two blank lines.
- Render standalone quotes—often written as `*„text”*`—with `blockquote_avatar`. Follow existing interviews for exact usage.
- Fix markup typos. Replace accidental double spaces after ordinary sentences with one space.
- Replace `...` with `…`.
