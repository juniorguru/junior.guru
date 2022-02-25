from invoke import task


@task()
def freeze(context):
    context.run('python -m juniorguru.web')


@task()
def mkdocs(context):
    context.run('mkdocs build --config-file=juniorguru/mkdocs/mkdocs.yml --site-dir=../../public/mkdocs')


@task()
def build(context):
    context.run('npx gulp build')


@task()
def serve(context):
    context.run('npx gulp serve')
