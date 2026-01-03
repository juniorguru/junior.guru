# CSS

Bootstrap 5 with custom SCSS styles, bundled via esbuild.

## Build Pipeline

1. **SCSS compilation** - esbuild-sass-plugin compiles SCSS to CSS
2. **Bundling & minification** - esbuild bundles and minifies
3. **Tree-shaking** - PurgeCSS removes unused CSS rules (production only)

Output: `public/static/css/index.css`

## Commands

```bash
jg web build                # Full build with CSS purging
jg web build --no-purge     # Skip CSS purging
jg web serve                # Dev server (no purging, fast rebuilds)
jg web serve --css-purge    # Dev server with CSS purging
```

## PurgeCSS

PurgeCSS scans generated HTML and removes CSS rules not found in the markup. This reduces CSS size significantly (~75% for this project).

**Safelisted classes** (toggled by JS, not in static HTML):
- `active` - tag selection state in filters
- `matching` - highlighting matching tags
- `open` - expanded job/candidate cards
- `noscript` - removed when JS loads

To add new JS-toggled classes, update the safelist in `src/jg/coop/cli/web.py`.
