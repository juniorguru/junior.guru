from subprocess import run, PIPE

import arrow

from juniorguru.lib.timer import measure
from juniorguru.models import LastModified, with_db


FILES = [
    'juniorguru/mkdocs/docs/candidate-handbook.md',
]


@measure()
@with_db
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


if __name__ == '__main__':
    main()
