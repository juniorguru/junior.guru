import pytest

from jg.coop.lib.youtube import parse_youtube_id


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=0v5K4GvK4Gs", "0v5K4GvK4Gs"),
        ("https://youtu.be/0v5K4GvK4Gs", "0v5K4GvK4Gs"),
        (
            "https://www.youtube.com/watch?v=3-wsqhCK-wU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_&index=5",
            "3-wsqhCK-wU",
        ),
    ],
)
def test_parse_yt_id(url, expected):
    assert parse_youtube_id(url) == expected


def test_parse_yt_id_raises():
    with pytest.raises(ValueError):
        parse_youtube_id("https://junior.guru")
