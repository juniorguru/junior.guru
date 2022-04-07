from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.models.story import Story


@pytest.fixture
def db_connection():
    db = SqliteDatabase(':memory:')
    with db:
        Story.bind(db)
        Story.create_table()
        yield db
        Story.drop_table()


def create_story(**kwargs):
    return Story.create(
        url=kwargs.get('url', 'https://blog.example.com/how-i-learned-to-code/'),
        date=kwargs.get('date', date(2019, 12, 19)),
        title=kwargs.get('title', 'How I Learned to Code'),
        image_path=kwargs.get('image', 'images/stories/somebody-something.jpg'),
        tags=kwargs.get('tags', [])
    )


def test_listing_sorts_by_date_desc(db_connection):
    story1 = create_story(date=date(2010, 7, 6))
    story2 = create_story(date=date(2019, 7, 6))
    story3 = create_story(date=date(2014, 7, 6))

    assert list(Story.listing()) == [story2, story3, story1]


def test_tag_listing(db_connection):
    story1 = create_story(tags=['science', 'age'])
    story2 = create_story(tags=['science', 'careerswitch'])  # noqa
    story3 = create_story(tags=['age', 'careerswitch'])

    assert set(Story.tag_listing('age')) == {story1, story3}


def test_tags_mapping(db_connection):
    story1 = create_story(date=date(2010, 7, 6), tags=['science', 'age'])
    story2 = create_story(date=date(2019, 7, 6), tags=['science', 'careerswitch'])
    story3 = create_story(date=date(2014, 7, 6), tags=['age', 'careerswitch'])
    mapping = Story.tags_mapping()

    assert set(mapping.keys()) == {'age', 'science', 'careerswitch'}
    assert mapping['age'] == [story3, story1]
    assert mapping['science'] == [story2, story1]
    assert mapping['careerswitch'] == [story2, story3]


@pytest.mark.parametrize('url,expected', (
    ('https://blog.example.com/foo-bar', 'blog.example.com'),
    ('http://www.example.com/foo-bar?moo=1#hell=o', 'example.com'),
    ('https://www.exAMPLE.com/', 'example.com'),
))
def test_publisher(db_connection, url, expected):
    assert create_story(url=url).publisher == expected
