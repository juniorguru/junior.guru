import pytest

from juniorguru.sync.subscriptions_csv import (
    classify_marketing_survey_answer,
    classify_referrer,
)


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://junior.guru/", "/"),
        ("https://junior.guru/learn/", "/learn"),
        (
            "https://junior.guru/events/?fbclid=IwAR0WkuqPqg7z6GHW-vEGgWlhgpzcT62qJkarSOrOQTsUjzxRBbSS8RGMw8I",
            "/events",
        ),
        ("https://t.co", "twitter"),
        ("https://t.co/RExQZc2z4V?amp=1", "twitter"),
        ("https://www.linkedin.com/", "linkedin"),
        ("https://l.facebook.com/", "facebook"),
        ("http://m.facebook.com", "facebook"),
        ("android-app://m.facebook.com/", "facebook"),
        ("https://honzajavorek.cz/", "honzajavorek"),
        (
            "https://honzajavorek.cz/blog/tydenni-poznamky-37-prvni-klubovy-sraz/",
            "honzajavorek",
        ),
        ("https://www.youtube.com/", "youtube"),
        ("https://www.google.com", "google"),
        ("https://www.patreon.com/", "other"),
    ],
)
def test_classify_referrer(url, expected):
    assert classify_referrer(url) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Google", "search"),
        ("Youtube", "youtube"),
        ('Youtube videá od "Yablko"', "yablko"),
        ("Cez video od yablka.", "yablko"),
        ("bla bla", "other"),
    ],
)
def test_classify_marketing_survey_answer(text, expected):
    assert classify_marketing_survey_answer(text) == expected
