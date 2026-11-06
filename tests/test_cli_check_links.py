from datetime import UTC, datetime

import pytest

from jg.coop.cli.check_links import (
    format_status,
    get_persistent_failures,
    parse_failures,
    update_history,
)


REPORT = {
    "error_map": {
        "public/podcast/index.html": [
            {
                "url": "https://example.com/404",
                "status": {"text": "404 Not Found", "code": 404},
            },
        ],
        "public/handbook/cv/index.html": [
            {
                "url": "https://example.com/404",
                "status": {"text": "404 Not Found", "code": 404},
            },
        ],
    },
    "timeout_map": {
        "public/index.html": [
            {
                "url": "https://slow.example.com/",
                "status": {"text": "Timeout", "details": "Request timed out"},
            },
        ],
    },
    "excluded_map": {
        "public/index.html": [
            {"url": "https://www.youtube.com/", "status": {"text": "Excluded"}},
        ],
    },
}


def test_parse_failures():
    assert parse_failures(REPORT) == {
        "https://example.com/404": {
            "status": "404 Not Found",
            "sources": [
                "public/handbook/cv/index.html",
                "public/podcast/index.html",
            ],
        },
        "https://slow.example.com/": {
            "status": "Timeout: Request timed out",
            "sources": ["public/index.html"],
        },
    }


def test_parse_failures_empty_report():
    assert parse_failures({"total": 0}) == {}


@pytest.mark.parametrize(
    "status, expected",
    [
        ({"text": "404 Not Found", "code": 404}, "404 Not Found"),
        (
            {"text": "Timeout", "details": "Request timed out"},
            "Timeout: Request timed out",
        ),
    ],
)
def test_format_status(status: dict, expected: str):
    assert format_status(status) == expected


def test_update_history_appends():
    history = [
        {"checked_at": "2026-11-01T04:00:00+00:00", "urls": ["https://a.example.com/"]}
    ]
    failures = {"https://b.example.com/": {}, "https://a.example.com/": {}}

    assert update_history(
        history, failures, datetime(2026, 11, 2, 4, tzinfo=UTC), 3
    ) == [
        {"checked_at": "2026-11-01T04:00:00+00:00", "urls": ["https://a.example.com/"]},
        {
            "checked_at": "2026-11-02T04:00:00+00:00",
            "urls": ["https://a.example.com/", "https://b.example.com/"],
        },
    ]


def test_update_history_keeps_only_last_runs():
    history = [{"checked_at": str(day), "urls": []} for day in range(1, 4)]
    new_history = update_history(history, {}, datetime(2026, 11, 4, tzinfo=UTC), 3)

    assert [entry["checked_at"] for entry in new_history] == [
        "2",
        "3",
        "2026-11-04T00:00:00+00:00",
    ]


def test_get_persistent_failures():
    history = [
        {"urls": ["https://a.example.com/", "https://b.example.com/"]},
        {
            "urls": [
                "https://a.example.com/",
                "https://b.example.com/",
                "https://c.example.com/",
            ]
        },
        {"urls": ["https://c.example.com/", "https://b.example.com/"]},
    ]

    assert get_persistent_failures(history, 3) == ["https://b.example.com/"]


def test_get_persistent_failures_looks_only_at_last_runs():
    history = [
        {"urls": []},
        {"urls": ["https://a.example.com/"]},
        {"urls": ["https://a.example.com/"]},
        {"urls": ["https://a.example.com/"]},
    ]

    assert get_persistent_failures(history, 3) == ["https://a.example.com/"]


def test_get_persistent_failures_short_history():
    history = [
        {"urls": ["https://a.example.com/"]},
        {"urls": ["https://a.example.com/"]},
    ]

    assert get_persistent_failures(history, 3) == []
