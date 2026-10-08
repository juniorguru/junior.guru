from datetime import date

import pytest

from jg.coop.sync.search_console import (
    get_complete_months,
    get_months_to_sync,
    is_significant,
    parse_row,
    pick_site_url,
    serialize_rows,
    shorten_url,
)


def test_get_complete_months():
    available_dates = [date(2025, 5, 14), date(2025, 6, 1), date(2025, 9, 28)]

    assert get_complete_months(available_dates) == [
        date(2025, 6, 1),
        date(2025, 7, 1),
        date(2025, 8, 1),
    ]


def test_get_complete_months_includes_month_ending_on_last_available_date():
    available_dates = [date(2025, 6, 1), date(2025, 6, 30)]

    assert get_complete_months(available_dates) == [date(2025, 6, 1)]


def test_get_complete_months_empty():
    assert get_complete_months([]) == []


def test_get_months_to_sync():
    months = [date(2025, 6, 1), date(2025, 7, 1), date(2025, 8, 1)]
    existing_months = {date(2025, 6, 1), date(2025, 8, 1)}

    assert get_months_to_sync(months, existing_months) == [date(2025, 7, 1)]


@pytest.mark.parametrize(
    "site_urls, expected",
    [
        (["https://junior.guru/", "sc-domain:junior.guru"], "sc-domain:junior.guru"),
        (["https://example.com/", "https://junior.guru/"], "https://junior.guru/"),
    ],
)
def test_pick_site_url(site_urls: list[str], expected: str):
    assert pick_site_url(site_urls) == expected


def test_pick_site_url_missing():
    with pytest.raises(ValueError):
        pick_site_url(["https://example.com/"])


def test_parse_row():
    row = {
        "keys": ["https://junior.guru/handbook/", "jak se naučit programovat"],
        "clicks": 12.0,
        "impressions": 345.0,
        "ctr": 0.0347,
        "position": 7.4562,
    }

    assert parse_row(row, ["page", "query"]) == {
        "page": "/handbook/",
        "query": "jak se naučit programovat",
        "clicks": 12,
        "impressions": 345,
        "position": 7.46,
    }


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://junior.guru/", "/"),
        ("https://junior.guru/handbook/", "/handbook/"),
        ("https://junior.guru/jobs/brno?page=2", "/jobs/brno?page=2"),
        ("https://junior.guru", "https://junior.guru"),
        ("http://junior.guru/handbook/", "http://junior.guru/handbook/"),
        ("https://www.junior.guru/handbook/", "https://www.junior.guru/handbook/"),
        ("https://junior.guru.example.com/", "https://junior.guru.example.com/"),
    ],
)
def test_shorten_url(url: str, expected: str):
    assert shorten_url(url) == expected


@pytest.mark.parametrize(
    "clicks, impressions, expected",
    [
        (0, 1, False),
        (0, 9, False),
        (0, 10, True),
        (1, 1, True),
    ],
)
def test_is_significant(clicks: int, impressions: int, expected: bool):
    row = {"clicks": clicks, "impressions": impressions}

    assert is_significant(row) is expected


def test_serialize_rows_is_sorted():
    rows = [
        {"page": "https://junior.guru/b", "clicks": 1},
        {"page": "https://junior.guru/a", "clicks": 2},
    ]

    assert serialize_rows(rows, ["page"]) == (
        '{"page": "https://junior.guru/a", "clicks": 2}\n'
        '{"page": "https://junior.guru/b", "clicks": 1}\n'
    )


def test_serialize_rows_keeps_unicode():
    rows = [{"query": "příručka", "clicks": 1}]

    assert serialize_rows(rows, ["query"]) == '{"query": "příručka", "clicks": 1}\n'
