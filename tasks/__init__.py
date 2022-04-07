import pytest
from invoke import Collection, task, Exit

from . import checks, web, sync
from .screenshots import screenshots


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


namespace = Collection(test, lint, screenshots, sync, web, checks)
