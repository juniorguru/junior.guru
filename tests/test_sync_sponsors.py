from datetime import date

import pytest

from jg.coop.sync.sponsors import get_coupons_mapping, get_renews_on, get_start_on


@pytest.mark.parametrize(
    "periods, today, expected",
    [
        pytest.param(
            [["2021-02", None]],
            date(2024, 6, 1),
            date(2025, 3, 1),
            id="no end, start before this month",
        ),
        pytest.param(
            [["2021-07", None]],
            date(2024, 6, 1),
            date(2024, 8, 1),
            id="no end, start after this month",
        ),
        pytest.param(
            [["2021-06", None]],
            date(2024, 6, 1),
            date(2025, 7, 1),
            id="no end, start this month",
        ),
        pytest.param(
            [["2021-02", "2024-02"]],
            date(2024, 6, 1),
            None,
            id="past",
        ),
        pytest.param(
            [["2021-07", "2024-07"]],
            date(2024, 6, 1),
            date(2024, 8, 1),
            id="future",
        ),
        pytest.param(
            [["2021-07", "2028-07"]],
            date(2024, 6, 1),
            date(2028, 8, 1),
            id="far future",
        ),
        pytest.param(
            [["2021-02", "2024-07"]],
            date(2024, 6, 1),
            date(2024, 8, 1),
            id="different starting and renew months",
        ),
        pytest.param(
            [["1999-02", "2001-02"], ["2021-02", None]],
            date(2024, 6, 1),
            date(2025, 3, 1),
            id="skips past periods",
        ),
    ],
)
def test_get_renews_on(
    periods: list[tuple[str, str | None]], today: date, expected: date
):
    assert get_renews_on(periods, today) == expected


@pytest.mark.parametrize(
    "periods, expected",
    [
        ([["2021-02", None]], date(2021, 2, 1)),
        ([["2021-02", None], ["1999-02", "2001-02"]], date(1999, 2, 1)),
    ],
)
def test_get_start_on(periods: list[tuple[str, str | None]], expected: date):
    assert get_start_on(periods) == expected


def test_get_coupons_mapping():
    assert get_coupons_mapping(
        [
            {"code": "FOO123123123", "state": "enabled"},
            {"code": "BOO456456456", "state": "enabled"},
            {"code": "MOO666666666", "state": "disabled"},
        ]
    ) == {
        "foo": "FOO123123123",
        "boo": "BOO456456456",
    }
