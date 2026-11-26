from datetime import date

import pytest

from jg.coop.sync.web_usage import (
    EVENTS_LIMIT,
    PAGES_LIMIT,
    aggregate_products,
    check_response,
    deserialize_rows,
    get_months,
    get_months_to_sync,
    parse_events,
    parse_pages,
    parse_range,
    serialize_rows,
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
        "events": [
            {"name": "github_profile_check", "total": 15},
            {"name": "github_profile_check_jobs", "total": 4},
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


@pytest.mark.parametrize(
    "start, end",
    [
        pytest.param(
            "2026-09-30T23:00:00.000Z", "2026-10-31T22:59:59.999Z", id="start"
        ),
        pytest.param("2026-09-30T22:00:00.000Z", "2026-10-31T21:59:59.999Z", id="end"),
    ],
)
def test_parse_range_not_aligned_to_days(start: str, end: str):
    with pytest.raises(ValueError, match="not aligned"):
        parse_range({"start": start, "end": end})


def test_parse_pages():
    data = create_response()

    assert parse_pages(data, date(2026, 10, 1), date(2026, 11, 1)) == [
        {"page": "/jobs", "pageviews": 7},
        {"page": "/", "pageviews": 3},
    ]


def test_check_response():
    data = create_response()

    assert check_response(data, date(2026, 10, 1), date(2026, 11, 1)) is None


@pytest.mark.parametrize("parse", [parse_pages, parse_events])
def test_parse_not_ok(parse):
    data = create_response(ok=False)

    with pytest.raises(ValueError, match="Unexpected"):
        parse(data, date(2026, 10, 1), date(2026, 11, 1))


@pytest.mark.parametrize("parse", [parse_pages, parse_events])
def test_parse_unexpected_range(parse):
    data = create_response(end="2026-10-30T22:59:59.999Z")

    with pytest.raises(ValueError, match="range"):
        parse(data, date(2026, 10, 1), date(2026, 11, 1))


def test_parse_pages_truncated():
    pages = [{"value": f"/{i}", "pageviews": 1} for i in range(PAGES_LIMIT)]
    data = create_response(pages=pages, pageviews=PAGES_LIMIT)

    with pytest.raises(ValueError, match="truncated"):
        parse_pages(data, date(2026, 10, 1), date(2026, 11, 1))


def test_parse_pages_sum_mismatch():
    data = create_response(pageviews=11)

    with pytest.raises(ValueError, match="sum up"):
        parse_pages(data, date(2026, 10, 1), date(2026, 11, 1))


def test_parse_events():
    data = create_response()

    assert parse_events(data, date(2026, 10, 1), date(2026, 11, 1)) == [
        {"name": "github_profile_check", "total": 15},
        {"name": "github_profile_check_jobs", "total": 4},
    ]


def test_parse_events_empty():
    data = create_response(events=[])

    assert parse_events(data, date(2026, 10, 1), date(2026, 11, 1)) == []


def test_parse_events_truncated():
    events = [{"name": f"event_{i}", "total": 1} for i in range(EVENTS_LIMIT)]
    data = create_response(events=events)

    with pytest.raises(ValueError, match="truncated"):
        parse_events(data, date(2026, 10, 1), date(2026, 11, 1))


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


def test_serialize_rows():
    pages = [
        {"page": "/jobs", "pageviews": 7},
        {"page": "/", "pageviews": 3},
    ]

    assert serialize_rows(pages, "page") == (
        '{"page": "/", "pageviews": 3}\n{"page": "/jobs", "pageviews": 7}\n'
    )


def test_serialize_rows_sorts_by_given_key():
    events = [
        {"name": "github_profile_check_jobs", "total": 4},
        {"name": "github_profile_check", "total": 15},
    ]

    assert serialize_rows(events, "name") == (
        '{"name": "github_profile_check", "total": 15}\n'
        '{"name": "github_profile_check_jobs", "total": 4}\n'
    )


def test_serialize_rows_keeps_unicode():
    pages = [{"page": "/čau", "pageviews": 1}]

    assert serialize_rows(pages, "page") == '{"page": "/čau", "pageviews": 1}\n'


def test_serialize_rows_empty():
    assert serialize_rows([], "name") == ""


def test_deserialize_rows_roundtrip():
    pages = [
        {"page": "/", "pageviews": 3},
        {"page": "/jobs", "pageviews": 7},
    ]

    assert deserialize_rows(serialize_rows(pages, "page")) == pages


def test_deserialize_rows_empty():
    assert deserialize_rows("") == []
