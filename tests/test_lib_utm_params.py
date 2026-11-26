import pytest

from jg.coop.lib.utm_params import (
    club_utm_params,
    get_utm_params,
    pick_utm_params,
    put_utm_params,
    strip_params,
)


@pytest.mark.parametrize(
    "url,param_names,expected",
    [
        ("https://example.com", ["a", "b"], "https://example.com"),
        ("https://example.com?a=1&b=2", ["a", "b"], "https://example.com"),
        ("https://example.com?a=1&c=3&b=2", ["a", "b"], "https://example.com?c=3"),
        ("https://example.com", [], "https://example.com"),
        ("https://example.com?a=1&b=2", [], "https://example.com?a=1&b=2"),
    ],
)
def test_strip_params(url, param_names, expected):
    assert strip_params(url, param_names) == expected


def test_get_utm_params():
    url = "https://example.com?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale&utm_term=shoes&utm_content=ad1&other_param=value"
    expected = {
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "spring_sale",
        "utm_term": "shoes",
        "utm_content": "ad1",
    }
    assert get_utm_params(url) == expected


def test_get_utm_params_empty_value():
    url = "https://example.com?utm_medium=&utm_campaign=spring_sale"
    expected = {
        "utm_campaign": "spring_sale",
    }
    assert get_utm_params(url) == expected


def test_put_utm_params():
    url = "https://example.com?other_param=value"
    utm_params = {
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "spring_sale",
    }
    expected = "https://example.com?other_param=value&utm_source=google&utm_medium=cpc&utm_campaign=spring_sale"

    assert put_utm_params(url, utm_params) == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ({}, {}),
        ({"referrer": "https://junior.guru/club/"}, {}),
        ({"utm_source": "", "utm_medium": None}, {}),
        (
            {"referrer": "https://junior.guru/", "utm_source": "x", "utm_medium": "y"},
            {"utm_source": "x", "utm_medium": "y"},
        ),
    ],
)
def test_pick_utm_params(params: dict, expected: dict):
    assert pick_utm_params(params) == expected


@pytest.mark.parametrize(
    "source, content, expected",
    [
        (
            "jobs-box",
            None,
            {"utm_source": "jobs-box", "utm_medium": "web", "utm_campaign": "jaro"},
        ),
        (
            "event-channel",
            42,
            {
                "utm_source": "event-channel",
                "utm_medium": "web",
                "utm_campaign": "jaro",
                "utm_content": "42",
            },
        ),
    ],
)
def test_club_utm_params(source: str, content: str | int | None, expected: dict):
    assert club_utm_params(source, content) == expected
