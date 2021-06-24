test:
	pipenv run pytest $(TESTOPTS)

lint:
	pipenv run flake8 && npx stylelint 'juniorguru/web/static/src/css-mkdocs/**/*.scss'

sync:
	pipenv run python -m juniorguru.sync $(SYNC)

freeze:
	pipenv run python -m juniorguru.web

mkdocs:
	pipenv run python -m mkdocs build --config-file=juniorguru/mkdocs/mkdocs.yml --site-dir=../../public/mkdocs

build:
	npx gulp build

send:
	pipenv run python -m juniorguru.send

screenshots:
	pipenv run python scripts/screenshots.py

check-links:
	pipenv run python scripts/check_links.py $(CHECKOPTS)

check-anchors:
	pipenv run python scripts/check_anchors.py

check-scrapers:
	pipenv run python scripts/check_scrapers.py

check-performance:
	pipenv run python scripts/check_performance.py

serve:
	npx gulp serve
