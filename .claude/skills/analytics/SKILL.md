---
name: analytics
description: Look up junior.guru web analytics (traffic, pageviews, visitors, top pages, referrers, countries, UTM sources, devices, events) via public Simple Analytics. Use whenever a task needs data about website visits or page popularity.
---

# Web Analytics

junior.guru uses [Simple Analytics](https://www.simpleanalytics.com/). Stats are public, no login or API key needed:

- Dashboard for humans: https://dashboard.simpleanalytics.com/junior.guru
- Stats API (JSON): `https://simpleanalytics.com/junior.guru.json`
- API docs: https://docs.simpleanalytics.com/api/stats (date placeholders: https://docs.simpleanalytics.com/api/helpers)

Prefer the API over scraping the dashboard.

## Querying the Stats API

Always send `version=6` and `info=false` (skips verbose field descriptions). Pick what you need via `fields`:

```bash
curl -sSL "https://simpleanalytics.com/junior.guru.json?version=6&info=false&start=2026-09-01&end=2026-10-01&fields=pageviews,visitors,pages&limit=20"
```

- Totals: `pageviews`, `visitors`.
- Time series: `histogram` with `interval=hour|day|week|month|year`.
- Breakdowns (lists of `{value, pageviews, visitors}`, sorted desc, capped by `limit` 1–1000): `pages`, `referrers`, `countries`, `utm_sources`, `utm_mediums`, `utm_campaigns`, `utm_contents`, `utm_terms`, `browser_names`, `os_names`, `device_types`.
- `seconds_on_page`: median time on page; also embedded into `pages` items.
- Custom events: `events=*` or `events=name1,name2`. The only event currently sent from the site is `github_profile_check` (see `src/jg/coop/js/github-profile.js`).

Dates:

- `start`/`end` as `YYYY-MM-DD` or placeholders like `today-30d`, `yesterday`, `today`. Default is the last month.
- Timezone is `Europe/Prague`. In practice `end` is exclusive: `start=2026-09-01&end=2026-10-01` covers all of September. Check `start`/`end` echoed in the response to be sure.
- Large ranges with breakdowns can take several seconds; use a generous timeout (the code uses 30s).

Filters: `page`, `pages` (comma-separated), `country`, `referrer`, `utm_source`, `device_type`, etc. Trailing `*` wildcards work, e.g. `page=/jobs/*`. Alternatively append the path to the URL: `https://simpleanalytics.com/junior.guru/club.json?...`. Contains-search (`*foo*`) needs an API key, which we don't use.

## junior.guru specifics

- Paths have no trailing slash on the live site, but some sections are tracked both ways. To cover a section fully, use e.g. `pages=/handbook,/handbook/,/handbook/*`. The canonical section grouping lives in `PRODUCTS` in `src/jg/coop/sync/web_usage.py` (home, club, handbook, courses, jobs, candidates, …).
- Main sections: `/jobs` (job board, by far the most traffic; city listings like `/jobs/brno`, individual jobs as `/jobs/<hash id>`), `/handbook/*`, `/courses/*` (course providers), `/club`, `/stories/*`, `/podcast/*`, `/events/*`.
- Traffic is mostly from Czechia (`cz`) and Slovakia (`sk`); top referrer is `google`.
- Existing code reading the API, use as reference before writing new code:
  - `src/jg/coop/sync/web_usage.py`: monthly pageviews per section, rendered at `/about/web-usage` (`src/jg/coop/web/docs/about/web-usage.md`).
  - `src/jg/coop/sync/course_providers.py`: pageviews of `/courses/*` pages.
  - `src/jg/coop/models/job.py`: builds a dashboard link filtered to one job (`?search=paths:<id>&start=…&end=…`).
- Never run `jg sync` just to get analytics. Query the API directly.
