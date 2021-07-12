from pathlib import Path

from strictyaml import Map, Optional, Seq, Str, Datetime, load

from juniorguru.lib.timer import measure
from juniorguru.models import PressRelease, db


schema = Seq(
    Map({
        'id': Str(),
        'date': Datetime(),
        'title': Str(),
        Optional('lead'): Str(),
        'text': Str(),
    })
)


@measure('press_releases')
def main():
    path = Path(__file__).parent.parent / 'data' / 'press_releases.yml'
    records = load(path.read_text(), schema).data

    with db:
        PressRelease.drop_table()
        PressRelease.create_table()

        for record in records:
            PressRelease.create(**record)


if __name__ == '__main__':
    main()
