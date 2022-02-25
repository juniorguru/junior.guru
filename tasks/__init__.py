import pytest
from invoke import Collection, task, Exit

from . import checks, web, sync


@task(incrementable=['v'])
def test(context, v=0, x=False):
    args = (v * ['-v']) + (int(x) * ['-x'])
    code = pytest.main(args)
    if code:
        raise Exit(code=code)


@task()
def lint(context):
    context.run('poetry run flake8')
    context.run("npx stylelint 'juniorguru/web/static/src/css-mkdocs/**/*.scss' 'juniorguru/image_templates/*.css'")


@task()
def send(context):
    context.run('python -m juniorguru.send')


@task()
def screenshots(context):
    context.run('python scripts/screenshots.py')


namespace = Collection(test, lint, send, screenshots, sync, web, checks)
