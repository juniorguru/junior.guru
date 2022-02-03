from datetime import date, timedelta

import pytest

from juniorguru.jobs.legacy_jobs.pipelines import sort_rank


@pytest.fixture
def oct_5():
    return date(2020, 10, 5)


def test_calc_sort_rank():
    assert sort_rank.calc_sort_rank({
        'param_a': 2,
        'param_b': 10,
    }, {
        'param_a': 1,
        'param_b': 2,
    }) == 22


@pytest.mark.parametrize('pricing_plan,expected', [
    (None, 0),
    ('community', 0),
    ('standard', 90),
    ('annual_flat_rate', 100),
])
def test_calc_sort_rank_favoritism_juniorguru(pricing_plan, expected):
    assert sort_rank.calc_favoritism(pricing_plan) == expected


@pytest.mark.parametrize('posted_at,today,expected', [
    (date(2020, 9, 1), date(2020, 9, 1) + timedelta(days=15), 50),
    (date(2020, 9, 1), date(2020, 9, 1) + timedelta(days=30), 100),
    (date(2020, 9, 1), date(2020, 9, 1) + timedelta(days=45), 50),
    (date(2020, 9, 1), date(2020, 9, 1) + timedelta(days=60), 100),
])
def test_calc_freshness(posted_at, today, expected):
    assert sort_rank.calc_freshness(posted_at, today) == expected


def test_calc_freshness_regular(oct_5):
    assert (sort_rank.calc_freshness(date(2020, 10, 1), oct_5)
            > sort_rank.calc_freshness(date(2020, 9, 10), oct_5))


def test_calc_freshness_monthly_bump(oct_5):
    assert (sort_rank.calc_freshness(date(2020, 9, 2), oct_5)
            > sort_rank.calc_freshness(date(2020, 10, 1), oct_5))


def test_calc_freshness_monthly_bump_equal(oct_5):
    assert (sort_rank.calc_freshness(date(2020, 9, 1), oct_5)
            == sort_rank.calc_freshness(date(2020, 10, 1), oct_5))


def test_calc_juniority():
    assert sort_rank.calc_juniority(10) > sort_rank.calc_juniority(5)


def test_calc_juniority_min():
    assert sort_rank.calc_juniority(-10) == sort_rank.calc_juniority(-1)


def test_calc_juniority_max():
    assert sort_rank.calc_juniority(20) == sort_rank.calc_juniority(30)
