from invoke import task


@task()
def links(context, retry=False):
    args = '--retry' if retry else ''
    context.run(f'python scripts/check_links.py {args}', pty=True)


@task()
def anchors(context):
    context.run('python scripts/check_anchors.py', pty=True)
