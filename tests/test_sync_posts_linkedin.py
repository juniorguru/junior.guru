import json

import pytest

from jg.coop.sync.posts_linkedin import (
    get_post_filename,
    parse_posted_at,
    serialize_post,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2026-05-26T14:09:00Z", "2026-05-26T14-09.json"),
        ("2026-05-26T14:09:00+02:00", "2026-05-26T14-09.json"),
        ("2026-05-26 14:09:00", "2026-05-26T14-09.json"),
    ],
)
def test_get_post_filename(value: str, expected: str):
    post = {"postedAtISO": value}
    assert get_post_filename(post) == expected


def test_parse_posted_at_invalid():
    with pytest.raises(ValueError):
        parse_posted_at("not-a-date")


def test_serialize_post_removes_tracking_id_recursively():
    post = {
        "trackingId": "root",
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "meta": {
            "trackingId": "nested",
            "author": "Honza",
            "items": [
                {"name": "a", "trackingId": "item-a"},
                {"name": "b", "children": [{"trackingId": "child-b"}]},
                "plain",
            ],
        },
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "meta": {
            "author": "Honza",
            "items": [
                {"name": "a"},
                {"name": "b", "children": [{}]},
                "plain",
            ],
        },
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_strips_query_from_post_level_url_only():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "url": "https://www.linkedin.com/posts/honzajavorek_example-activity-1?utm_source=combined_share_message&utm_medium=member_desktop&rcm=foo",
        "article": {
            "url": "https://www.linkedin.com/pulse/example-article?trackingId=abc123"
        },
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "url": "https://www.linkedin.com/posts/honzajavorek_example-activity-1",
        "article": {
            "url": "https://www.linkedin.com/pulse/example-article?trackingId=abc123"
        },
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_strips_t_param_from_image_urls():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "picture": "https://media.licdn.com/dms/image/v2/C4E03AQHmtgVOIg7GeQ/profile.jpg?e=1781136000&v=beta&t=abc123",
        "nested": {
            "backgroundImage": "https://media.licdn.com/dms/image/v2/D4E16AQFjcB6YDMjwHg/background.jpg?e=1781136000&v=beta&t=def456",
            "nonImageUrl": "https://example.com/image.jpg?e=1&v=beta&t=keepme",
        },
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "picture": "https://media.licdn.com/dms/image/v2/C4E03AQHmtgVOIg7GeQ/profile.jpg?e=1781136000&v=beta",
        "nested": {
            "backgroundImage": "https://media.licdn.com/dms/image/v2/D4E16AQFjcB6YDMjwHg/background.jpg?e=1781136000&v=beta",
            "nonImageUrl": "https://example.com/image.jpg?e=1&v=beta&t=keepme",
        },
    }

    assert json.loads(serialize_post(post)) == expected
