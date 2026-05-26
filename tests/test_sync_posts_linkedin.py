import pytest

from jg.coop.sync.posts_linkedin import get_post_filename, parse_posted_at


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
