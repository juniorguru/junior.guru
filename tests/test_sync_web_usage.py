from datetime import date

import pytest

from jg.coop.sync.web_usage import (
    PAGES_LIMIT,
    aggregate_products,
    deserialize_pages,
    get_months,
    get_months_to_sync,
    parse_pages,
    parse_range,
    serialize_pages,
)


def create_response(**kwargs) -> dict:
    return {
        "ok": True,
        "start": "2026-09-30T22:00:00.000Z",
        "end": "2026-10-31T22:59:59.999Z",
        "timezone": "Europe/Prague",
        "pageviews": 10,
        "pages": [
            {"value": "/jobs", "pageviews": 7, "visitors": 3},
            {"value": "/", "pageviews": 3, "visitors": 2},
        ],
    } | kwargs


def test_get_months():
    assert get_months(date(2026, 11, 24), 3) == [
        date(2026, 8, 1),
        date(2026, 9, 1),
        date(2026, 10, 1),
    ]


def test_get_months_on_first_day_of_month():
    assert get_months(date(2026, 11, 1), 1) == [date(2026, 10, 1)]


def test_get_months_across_years():
    assert get_months(date(2026, 2, 15), 3) == [
        date(2025, 11, 1),
        date(2025, 12, 1),
        date(2026, 1, 1),
    ]


def test_get_months_to_sync():
    months = [date(2026, 8, 1), date(2026, 9, 1), date(2026, 10, 1)]
    existing_months = {date(2026, 9, 1), date(2025, 1, 1)}

    assert get_months_to_sync(months, existing_months) == [
        date(2026, 8, 1),
        date(2026, 10, 1),
    ]


@pytest.mark.parametrize(
    "start, end, expected",
    [
        pytest.param(
            "2026-09-30T22:00:00.000Z",
            "2026-10-31T22:59:59.999Z",
            (date(2026, 10, 1), date(2026, 11, 1)),
            id="october-dst-change",
        ),
        pytest.param(
            "2025-12-31T23:00:00.000Z",
            "2026-01-31T22:59:59.999Z",
            (date(2026, 1, 1), date(2026, 2, 1)),
            id="january-winter-time",
        ),
        pytest.param(
            "2026-06-30T22:00:00.000Z",
            "2026-07-31T21:59:59.999Z",
            (date(2026, 7, 1), date(2026, 8, 1)),
            id="july-summer-time",
        ),
    ],
)
def test_parse_range(start: str, end: str, expected: tuple[date, date]):
    assert parse_range({"start": start, "end": end}) == expected


def test_parse_range_not_aligned_to_days():
    with pytest.raises(ValueError, match="not aligned"):
        parse_range(
            {"start": "2026-09-30T23:00:00.000Z", "end": "2026-10-31T22:59:59.999Z"}
        )


def test_parse_pages():
    data = create_response()

    assert parse_pages(data, date(2026, 10, 1), date(2026, 11, 1)) == [
        {"page": "/jobs", "pageviews": 7},
        {"page": "/", "pageviews": 3},
    ]


def test_parse_pages_not_ok():
    data = create_response(ok=False)

    with pytest.raises(ValueError, match="Unexpected"):
        parse_pages(data, date(2026, 10, 1), date(2026, 11, 1))


def test_parse_pages_unexpected_range():
    data = create_response(end="2026-10-30T22:59:59.999Z")

    with pytest.raises(ValueError, match="range"):
        parse_pages(data, date(2026, 10, 1), date(2026, 11, 1))


def test_parse_pages_truncated():
    pages = [{"value": f"/{i}", "pageviews": 1} for i in range(PAGES_LIMIT)]
    data = create_response(pages=pages, pageviews=PAGES_LIMIT)

    with pytest.raises(ValueError, match="truncated"):
        parse_pages(data, date(2026, 10, 1), date(2026, 11, 1))


def test_parse_pages_sum_mismatch():
    data = create_response(pageviews=11)

    with pytest.raises(ValueError, match="sum up"):
        parse_pages(data, date(2026, 10, 1), date(2026, 11, 1))


@pytest.mark.parametrize(
    "page, patterns, expected",
    [
        ("/jobs", ["*"], 1),
        ("/", ["/"], 1),
        ("/jobs", ["/"], 0),
        ("/club", ["/club", "/club/"], 1),
        ("/club/", ["/club", "/club/"], 1),
        ("/clubhouse", ["/club", "/club/"], 0),
        ("/handbook/cv", ["/handbook/*"], 1),
        ("/handbook/cv/extra", ["/handbook/*"], 1),
        ("/handbookish", ["/handbook", "/handbook/", "/handbook/*"], 0),
        ("/Handbook/cv", ["/handbook/*"], 0),
    ],
)
def test_aggregate_products_matching(page: str, patterns: list[str], expected: int):
    pages = [{"page": page, "pageviews": 1}]

    assert aggregate_products(pages, {"product": patterns}) == {"product": expected}


def test_aggregate_products():
    pages = [
        {"page": "/", "pageviews": 5},
        {"page": "/jobs", "pageviews": 7},
        {"page": "/jobs/praha", "pageviews": 2},
        {"page": "/about", "pageviews": 1},
    ]
    products = {"total": ["*"], "home": ["/"], "jobs": ["/jobs", "/jobs/*"]}

    assert aggregate_products(pages, products) == {
        "total": 15,
        "home": 5,
        "jobs": 9,
    }


def test_aggregate_products_counts_page_once_per_product():
    pages = [{"page": "/jobs/", "pageviews": 3}]

    assert aggregate_products(pages, {"jobs": ["/jobs/", "/jobs/*"]}) == {"jobs": 3}


def test_serialize_pages():
    pages = [
        {"page": "/jobs", "pageviews": 7},
        {"page": "/", "pageviews": 3},
    ]

    assert serialize_pages(pages) == (
        '{"page": "/", "pageviews": 3}\n{"page": "/jobs", "pageviews": 7}\n'
    )


def test_serialize_pages_keeps_unicode():
    pages = [{"page": "/čau", "pageviews": 1}]

    assert serialize_pages(pages) == '{"page": "/čau", "pageviews": 1}\n'


def test_deserialize_pages_roundtrip():
    pages = [
        {"page": "/", "pageviews": 3},
        {"page": "/jobs", "pageviews": 7},
    ]

    assert deserialize_pages(serialize_pages(pages)) == pages


def test_deserialize_pages_empty():
    assert deserialize_pages("") == []
