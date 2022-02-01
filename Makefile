test:
	poetry run pytest $(TESTOPTS)

lint:
	poetry run flake8 && npx stylelint 'juniorguru/web/static/src/css-mkdocs/**/*.scss' 'juniorguru/image_templates/*.css'

jobs:
	poetry run python -m juniorguru.jobs

sync:
	poetry run python -m juniorguru.sync $(SYNC)

sync-jobs:
	poetry run python -m juniorguru.sync.jobs

freeze:
	poetry run python -m juniorguru.web

mkdocs:
	poetry run python -m mkdocs build --config-file=juniorguru/mkdocs/mkdocs.yml --site-dir=../../public/mkdocs

build:
	npx gulp build

send:
	poetry run python -m juniorguru.send

screenshots:
	poetry run python scripts/screenshots.py

check-links:
	poetry run python scripts/check_links.py $(CHECKOPTS)

check-anchors:
	poetry run python scripts/check_anchors.py

serve:
	npx gulp serve
