from datetime import date

import pytest

from jg.coop.sync.weekly_plans import parse_week


@pytest.mark.parametrize(
    "thread_name, today, expected",
    [
        ("Týden 5-11.2.", date(2024, 2, 5), date(2024, 2, 5)),
        ("Týden 6-11.2.", date(2024, 2, 6), date(2024, 2, 5)),
        ("Týden 15-21.1.", date(2024, 1, 15), date(2024, 1, 15)),
        ("Týden 29.1. - 4.2.", date(2024, 1, 29), date(2024, 1, 29)),
        ("Týden 27.11. - 3.12.", date(2023, 11, 27), date(2023, 11, 27)),
        ("Týden 2-8.1. 2023", date(2023, 1, 2), date(2023, 1, 2)),
        ("Týden 3-9.1. 2000", date(2023, 1, 3), date(2000, 1, 3)),
        ("Týden 18. - 24. 9.", date(2023, 9, 18), date(2023, 9, 18)),
        ("Týden 22-28.1", date(2024, 1, 22), date(2024, 1, 22)),
        # Year boundary: in January, December thread should use previous year
        ("Týden 30.12. - 5.1.", date(2025, 1, 2), date(2024, 12, 30)),
        ("Týden 30.12. - 5.1.", date(2025, 1, 5), date(2024, 12, 30)),
        # Year boundary: in December, December thread should use current year
        ("Týden 30.12. - 5.1.", date(2024, 12, 30), date(2024, 12, 30)),
        ("Týden 30.12. - 5.1.", date(2024, 12, 31), date(2024, 12, 30)),
    ],
)
def test_parse_week(thread_name: str, today: date, expected: date):
    assert parse_week(thread_name, today) == expected


def test_parse_week_raises():
    with pytest.raises(ValueError):
        parse_week("Týden posvátného pečení chleba", date(2000, 1, 1))
