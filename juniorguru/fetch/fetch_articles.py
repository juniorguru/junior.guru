from pathlib import Path

from strictyaml import load, Map, Datetime, Url, Str, Seq

from ..models import db, Article


schema = Seq(
    Map({
        'url': Url(),
        'date': Datetime(),
        'title': Str(),
    })
)


def main():
    path = Path(__file__).parent.parent / 'data' / 'articles.yml'
    records = [record.data for record in load(path.read_text(), schema)]

    with db:
        Article.drop_table()
        Article.create_table()

        for record in records:
            Article.create(**record)


if __name__ == '__main__':
    main()
