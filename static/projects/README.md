# Projects

Images of candidates' projects. Either images scraped from the project READMEs or screenshots of live demos. Populated by `jg sync candidates`.

To edit the default project image, edit the source `default-project.svg` (inside parent directory) and then run:

```bash
magick -density 300 src/jg/coop/images/default-project.svg -resize 1280 -quality 80 src/jg/coop/images/projects/default.webp
```
