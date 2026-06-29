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


def test_serialize_post_strips_all_query_from_post_level_url():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "url": "https://www.linkedin.com/posts/honzajavorek_example-activity-1?utm_source=combined_share_message&utm_medium=member_desktop&rcm=foo",
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "url": "https://www.linkedin.com/posts/honzajavorek_example-activity-1",
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_pops_tracking_id_from_nested_urls():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "article": {
            "url": "https://www.linkedin.com/pulse/example-article?trackingId=abc123"
        },
        "items": [
            {"url": "https://www.linkedin.com/pulse/foo?a=1&trackingId=xyz&b=2"},
        ],
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "article": {"url": "https://www.linkedin.com/pulse/example-article"},
        "items": [
            {"url": "https://www.linkedin.com/pulse/foo?a=1&b=2"},
        ],
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_preserves_double_encoded_url_when_popping_tracking_id():
    url = (
        "https://www.linkedin.com/pulse/"
        "t%25C3%25BDdenn%25C3%25AD-pozn%25C3%25A1mky-honza-javorek-elppf"
    )
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "article": {"url": f"{url}?trackingId=VcxvKxDjSSyxXaBRuxk66A%3D%3D"},
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "article": {"url": url},
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_drops_time_since_posted_recursively():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "timeSincePosted": "3mo",
        "meta": {
            "timeSincePosted": "3mo",
            "items": [{"timeSincePosted": "1w"}, "plain"],
        },
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "meta": {"items": [{}, "plain"]},
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_keeps_non_media_urls():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "nested": {
            "nonImageUrl": "https://example.com/image.jpg?e=1&v=beta&t=keepme",
        },
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "nested": {
            "nonImageUrl": "https://example.com/image.jpg?e=1&v=beta&t=keepme",
        },
    }

    assert json.loads(serialize_post(post)) == expected


def test_serialize_post_drops_volatile_media_urls_recursively():
    post = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "picture": "https://media.licdn.com/dms/image/v2/C4E03AQH/profile.jpg?e=1&v=beta&t=abc",
        "nested": {
            "backgroundImage": "https://media.licdn.com/dms/image/v2/D4E16AQF/background.jpg?e=1&v=beta&t=def",
            "list": [
                "https://media.licdn.com/dms/image/v2/C4E03AQH/another.jpg?e=1&v=beta&t=ghi",
                "https://example.com/static.jpg?e=1&v=beta&t=keep",
            ],
        },
    }
    expected = {
        "postedAtISO": "2026-05-21T19:53:23.509Z",
        "nested": {
            "list": [
                "https://example.com/static.jpg?e=1&v=beta&t=keep",
            ]
        },
    }

    assert json.loads(serialize_post(post)) == expected
