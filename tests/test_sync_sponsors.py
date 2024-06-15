from datetime import date

import pytest

from jg.coop.sync.sponsors import renew_date


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
            date(2024, 7, 1),
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
def test_renew_date(periods: list[tuple[str, str | None]], today: date, expected: date):
    assert renew_date(periods, today) == expected
