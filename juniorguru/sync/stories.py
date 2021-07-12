from pathlib import Path

from strictyaml import Datetime, Map, Seq, Str, Url, load

from juniorguru.lib.timer import measure
from juniorguru.models import Story, db


schema = Seq(
    Map({
        'url': Url(),
        'date': Datetime(),
        'title': Str(),
        'image_path': Str(),
        'tags': Seq(Str()),
    })
)


@measure('stories')
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
