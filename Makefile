test:
	poetry run pytest $(TESTOPTS)

lint:
	poetry run flake8 && npx stylelint 'juniorguru/web/static/src/css-mkdocs/**/*.scss' 'juniorguru/image_templates/*.css'

sync:
	poetry run python -m juniorguru.sync $(SYNC)

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

check-scrapers:
	poetry run python scripts/check_scrapers.py

check-performance:
	poetry run python scripts/check_performance.py

serve:
	npx gulp serve
