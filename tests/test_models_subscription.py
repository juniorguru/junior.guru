from datetime import date
from types import SimpleNamespace

import pytest

from jg.coop.models.subscription import count_by_month_and_source, count_by_source


def campaign(utm_source: str, account_total_spend: int) -> SimpleNamespace:
    return SimpleNamespace(utm_source=utm_source, is_payer=account_total_spend > 0)


def test_count_by_source():
    campaigns = [
        campaign("gh-check", 0),
        campaign("winback", 500),
        campaign("gh-check", 199),
        campaign("gh-check", 0),
    ]

    assert count_by_source(campaigns) == {
        "gh-check": {"trials": 3, "payers": 1},
        "winback": {"trials": 1, "payers": 1},
    }


def test_count_by_source_sorts_by_trials():
    campaigns = [campaign("a", 0), campaign("b", 0), campaign("b", 0)]

    assert list(count_by_source(campaigns)) == ["b", "a"]


def test_count_by_source_empty():
    assert count_by_source([]) == {}


MONTHS = [date(2026, 11, 30), date(2026, 12, 31), date(2027, 1, 12)]


def signup(utm_source: str, created_on: date) -> SimpleNamespace:
    return SimpleNamespace(utm_source=utm_source, created_on=created_on)


def test_count_by_month_and_source():
    campaigns = [
        signup("gh-check", date(2026, 11, 3)),
        signup("gh-check", date(2026, 11, 30)),
        signup("jobs-box", date(2026, 12, 1)),
        signup("gh-check", date(2027, 1, 5)),
    ]

    assert count_by_month_and_source(campaigns, MONTHS) == {
        "gh-check": [2, 0, 1],
        "jobs-box": [0, 1, 0],
    }


def test_count_by_month_and_source_counts_current_month_until_today():
    campaigns = [signup("gh-check", date(2027, 1, 20))]

    assert count_by_month_and_source(campaigns, MONTHS) == {"gh-check": [0, 0, 1]}


@pytest.mark.parametrize(
    "created_on", [date(2026, 10, 31), date(2027, 2, 1), date(2025, 11, 15)]
)
def test_count_by_month_and_source_ignores_other_months(created_on: date):
    campaigns = [signup("gh-check", created_on)]

    assert count_by_month_and_source(campaigns, MONTHS) == {}


def test_count_by_month_and_source_orders_by_first_signup():
    campaigns = [
        signup("winback", date(2027, 1, 2)),
        signup("jobs-box", date(2026, 12, 9)),
        signup("gh-check", date(2026, 12, 9)),
        signup("winback", date(2027, 1, 3)),
        signup("jobs-manual", date(2026, 11, 20)),
    ]

    assert list(count_by_month_and_source(campaigns, MONTHS)) == [
        "jobs-manual",
        "gh-check",
        "jobs-box",
        "winback",
    ]


def test_count_by_month_and_source_empty():
    assert count_by_month_and_source([], MONTHS) == {}
