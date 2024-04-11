from datetime import date

import pytest

from jg.coop.sync.weekly_plans import parse_week


@pytest.mark.parametrize(
    "thread_name, year, expected",
    [
        ("Týden 5-11.2.", 2024, date(2024, 2, 5)),
        ("Týden 6-11.2.", 2024, date(2024, 2, 5)),
        ("Týden 15-21.1.", 2024, date(2024, 1, 15)),
        ("Týden 29.1. - 4.2.", 2024, date(2024, 1, 29)),
        ("Týden 27.11. - 3.12.", 2023, date(2023, 11, 27)),
        ("Týden 2-8.1. 2023", 2023, date(2023, 1, 2)),
        ("Týden 3-9.1. 2000", 2023, date(2000, 1, 3)),
        ("Týden 18. - 24. 9.", 2023, date(2023, 9, 18)),
        ("Týden 22-28.1", 2024, date(2024, 1, 22)),
    ],
)
def test_parse_week(thread_name: str, year: int, expected: date):
    assert parse_week(thread_name, year) == expected


def test_parse_week_raises():
    with pytest.raises(ValueError):
        parse_week("Týden posvátného pečení chleba", 2000)
