from datetime import datetime

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Article


@pytest.fixture
def db():
    db = SqliteDatabase(':memory:')
    with db:
        Article.bind(db)
        Article.create_table()
        yield db
        Article.drop_table()


def create_article(**kwargs):
    return Article.create(
        url=kwargs.get('url', 'https://blog.example.com/how-i-learned-to-code/'),
        date=kwargs.get('date', datetime(2019, 12, 19, 0, 0, 0)),
        title=kwargs.get('title', 'How I Learned to Code'),
    )


def test_listing_sorts_by_date_desc(db):
    article1 = create_article(date=datetime(2010, 7, 6, 20, 24, 3))
    article2 = create_article(date=datetime(2019, 7, 6, 20, 24, 3))
    article3 = create_article(date=datetime(2014, 7, 6, 20, 24, 3))

    assert list(Article.listing()) == [article2, article3, article1]


@pytest.mark.parametrize('url,expected', (
    ('https://blog.example.com/foo-bar', 'blog.example.com'),
    ('http://www.example.com/foo-bar?moo=1#hell=o', 'example.com'),
    ('https://www.exAMPLE.com/', 'example.com'),
))
def test_publisher(db, url, expected):
    assert create_article(url=url).publisher == expected
