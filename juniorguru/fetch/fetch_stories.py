from pathlib import Path

from strictyaml import load, Map, Datetime, Url, Str, Seq

from ..models import db, Story


schema = Seq(
    Map({
        'url': Url(),
        'date': Datetime(),
        'title': Str(),
        'image_path': Str(),
    })
)


def main():
    path = Path(__file__).parent.parent / 'data' / 'stories.yml'
    records = [record.data for record in load(path.read_text(), schema)]

    with db:
        Story.drop_table()
        Story.create_table()

        for record in records:
            Story.create(**record)


if __name__ == '__main__':
    main()
