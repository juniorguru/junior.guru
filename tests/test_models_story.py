from datetime import date

import pytest

from jg.coop.models.story import Story

from testing_utils import prepare_test_db


@pytest.fixture
def test_db():
    yield from prepare_test_db([Story])


def create_story(**kwargs):
    return Story.create(
        url=kwargs.get("url", "https://blog.example.com/how-i-learned-to-code/"),
        date=kwargs.get("date", date(2019, 12, 19)),
        title=kwargs.get("title", "How I Learned to Code"),
        name=kwargs.get("name", "Fernando Alonso"),
        image_path=kwargs.get("image", "avatars-stories/somebody-something.jpg"),
        tags=kwargs.get("tags", []),
    )


def test_listing_sorts_by_date_desc(test_db):
    story1 = create_story(date=date(2010, 7, 6))
    story2 = create_story(date=date(2019, 7, 6))
    story3 = create_story(date=date(2014, 7, 6))

    assert list(Story.listing()) == [story2, story3, story1]


def test_tag_listing(test_db):
    story1 = create_story(tags=["science", "age"])
    create_story(tags=["science", "careerswitch"])
    story3 = create_story(tags=["age", "careerswitch"])

    assert set(Story.tag_listing("age")) == {story1, story3}


def test_tags_mapping(test_db):
    story1 = create_story(date=date(2010, 7, 6), tags=["science", "age"])
    story2 = create_story(date=date(2019, 7, 6), tags=["science", "careerswitch"])
    story3 = create_story(date=date(2014, 7, 6), tags=["age", "careerswitch"])
    mapping = Story.tags_mapping()

    assert set(mapping.keys()) == {"age", "science", "careerswitch"}
    assert mapping["age"] == [story3, story1]
    assert mapping["science"] == [story2, story1]
    assert mapping["careerswitch"] == [story2, story3]


@pytest.mark.parametrize(
    "url,expected",
    (
        ("https://blog.example.com/foo-bar", "blog.example.com"),
        ("http://www.example.com/foo-bar?moo=1#hell=o", "example.com"),
        ("https://www.exAMPLE.com/", "example.com"),
        (
            "https://web.archive.org/web/20250318124818/https://www.frantiseknemet.cz/posts/jak-jsem-se-stal-programatorem",
            "frantiseknemet.cz",
        ),
    ),
)
def test_publisher(test_db, url, expected):
    assert create_story(url=url).publisher == expected
