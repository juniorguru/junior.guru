import pytest

from jg.coop.lib.brand import site_url, static_url


@pytest.mark.parametrize(
    "path, expected",
    [
        ("", "https://junior.guru/"),
        ("events/1/", "https://junior.guru/events/1/"),
        ("/events/1/", "https://junior.guru/events/1/"),
    ],
)
def test_site_url(path: str, expected: str):
    assert site_url(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("logo.png", "https://junior.guru/static/logo.png"),
        ("/logo.png", "https://junior.guru/static/logo.png"),
    ],
)
def test_static_url(path: str, expected: str):
    assert static_url(path) == expected
