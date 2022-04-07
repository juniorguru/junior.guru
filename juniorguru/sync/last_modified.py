from subprocess import PIPE, run

import arrow

from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.last_modified import LastModified


FILES = [
    'juniorguru/mkdocs/docs/candidate-handbook.md',
]


@sync_task()
@db.connection_context()
def main():
    entries = []
    for path in FILES:
        result = run(['git', 'log', '-1', '--pretty=format:%ci', path],
                    stdout=PIPE, encoding='utf-8')
        value = arrow.get(result.stdout, 'YYYY-MM-DD HH:mm:ss Z')
        entries.append(dict(path=path, value=value.to('UTC').naive))

    LastModified.drop_table()
    LastModified.create_table()
    for entry in entries:
        LastModified.create(**entry)
