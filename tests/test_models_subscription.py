from types import SimpleNamespace

from jg.coop.models.subscription import count_by_source


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
