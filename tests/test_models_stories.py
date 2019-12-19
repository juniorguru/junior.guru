from datetime import datetime

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Story


@pytest.fixture
def db():
    db = SqliteDatabase(':memory:')
    with db:
        Story.bind(db)
        Story.create_table()
        yield db
        Story.drop_table()


def create_story(**kwargs):
    return Story.create(
        url=kwargs.get('url', 'https://blog.example.com/how-i-learned-to-code/'),
        date=kwargs.get('date', datetime(2019, 12, 19, 0, 0, 0)),
        title=kwargs.get('title', 'How I Learned to Code'),
    )


def test_listing_sorts_by_date_desc(db):
    story1 = create_story(date=datetime(2010, 7, 6, 20, 24, 3))
    story2 = create_story(date=datetime(2019, 7, 6, 20, 24, 3))
    story3 = create_story(date=datetime(2014, 7, 6, 20, 24, 3))

    assert list(Story.listing()) == [story2, story3, story1]


@pytest.mark.parametrize('url,expected', (
    ('https://blog.example.com/foo-bar', 'blog.example.com'),
    ('http://www.example.com/foo-bar?moo=1#hell=o', 'example.com'),
    ('https://www.exAMPLE.com/', 'example.com'),
))
def test_publisher(db, url, expected):
    assert create_story(url=url).publisher == expected
