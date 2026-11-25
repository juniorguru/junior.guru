from jg.coop.models.job import Tag, TagType
from jg.coop.sync.jobs_tags import get_tag_rows


def test_get_tag_rows():
    tags = [
        Tag(slug="remote", type=TagType.LOCATION),
        Tag(slug="python", type=TagType.TECHNOLOGY),
    ]

    assert get_tag_rows(42, tags) == [
        {"job": 42, "type": "location", "slug": "remote"},
        {"job": 42, "type": "technology", "slug": "python"},
    ]


def test_get_tag_rows_unique():
    tags = [
        Tag(slug="brno", type=TagType.LOCATION),
        Tag(slug="brno", type=TagType.LOCATION),
    ]

    assert get_tag_rows(42, tags) == [{"job": 42, "type": "location", "slug": "brno"}]


def test_get_tag_rows_empty():
    assert get_tag_rows(42, []) == []
