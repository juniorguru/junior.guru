from datetime import date

import pytest

from jg.coop.sync.subscriptions_csv import (
    Row,
    classify_marketing_survey_answer,
    classify_referrer,
    get_date,
    is_redacted_row,
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
        ("pres internet a to delsi dobu", "internet"),
        ("Na internetu", "internet"),
        ("Web", "internet"),
        ("Net", "internet"),
        ("Na nete", "internet"),
        ("webtrh.cz", "other"),
        ("Vyhodil mi ho webový prehliadač.", "other"),
        ("Našla jsem příručku.", "search"),
        ("Našel jsem si to sám", "search"),
        ("Z webu redhatu", "other"),
        ("z webu", "internet"),
        ("tip od sestry", "friend"),
        ("Nauč mě IT", "courses"),
        ("známý poslal odkaz", "friend"),
    ],
)
def test_classify_marketing_survey_answer(text, expected):
    assert classify_marketing_survey_answer(text) == expected


@pytest.mark.parametrize(
    "row, expected",
    [
        (
            {
                "Name": "N/A",
                "Email": "N/A",
                "Plan": "Členství v klubu",
                "Price (CZK)": "N/A",
                "Expiration Date": "N/A",
                "Reason": "",
                "Feedback": "",
            },
            True,
        ),
        (
            {
                "Name": "Aleš Novák",
                "Email": "alesnovak@example.com",
                "Plan": "Členství v klubu",
                "Price (CZK)": "299.00",
                "Expiration Date": "2025-02-23",
                "Reason": "Other",
                "Feedback": "",
            },
            False,
        ),
    ],
)
def test_is_redacted_row(row: Row, expected: bool):
    assert is_redacted_row(row) is expected


@pytest.mark.parametrize(
    "row, expected",
    [
        ({"Expiration Date": "2025-03-18"}, date(2025, 3, 18)),
        ({"Date": "2025-03-18"}, date(2025, 3, 18)),
        ({"Expiration Date": ""}, None),
        ({"Date": ""}, None),
        ({"Expiration Date": "N/A"}, None),
        ({"Date": "N/A"}, None),
    ],
)
def test_get_date(row: Row, expected: date | None):
    assert get_date(row) == expected
