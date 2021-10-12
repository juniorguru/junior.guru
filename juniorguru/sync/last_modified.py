from subprocess import run, PIPE

import arrow

from juniorguru.lib.timer import measure
from juniorguru.models import LastModified, db


FILES = [
    'juniorguru/web/templates/candidate_handbook.html',
    'juniorguru/mkdocs/docs/handbook/candidate-handbook.md',
]


@measure('last_modified')
def main():
    entries = []
    for path in FILES:
        result = run(['git', 'log', '-1', '--pretty=format:%ci', path],
                    stdout=PIPE, encoding='utf-8')
        value = arrow.get(result.stdout, 'YYYY-MM-DD HH:mm:ss Z')
        entries.append(dict(path=path, value=value.to('UTC').naive))

    with db:
        LastModified.drop_table()
        LastModified.create_table()
        for entry in entries:
            LastModified.create(**entry)


if __name__ == '__main__':
    main()
