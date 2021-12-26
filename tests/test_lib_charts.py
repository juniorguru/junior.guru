from datetime import date

import pytest

from juniorguru.lib import charts


def test_months():
    assert list(charts.months(date(2020, 1, 15), date(2020, 8, 30))) == [
        date(2020, 1, 31),
        date(2020, 2, 29),
        date(2020, 3, 31),
        date(2020, 4, 30),
        date(2020, 5, 31),
        date(2020, 6, 30),
        date(2020, 7, 31),
        date(2020, 8, 31),
    ]


@pytest.mark.parametrize('today, expected', [
    pytest.param(date(2021, 8, 30), (date(2020, 8, 30), date(2021, 8, 30)), id='random specific date'),
    pytest.param(date(2021, 12, 31), (date(2020, 12, 31), date(2021, 12, 31)), id='last day of the year'),
    pytest.param(date(2020, 2, 29), (date(2019, 2, 28), date(2020, 2, 29)), id='leap year #1'),
    pytest.param(date(2021, 2, 28), (date(2020, 2, 28), date(2021, 2, 28)), id='leap year #2'),
])
def test_ttm_range(today, expected):
    assert charts.ttm_range(today) == expected


@pytest.mark.parametrize('today, expected', [
    pytest.param(date(2021, 8, 30), (date(2021, 8, 1), date(2021, 8, 31)), id='random specific date'),
    pytest.param(date(2021, 2, 28), (date(2021, 2, 1), date(2021, 2, 28)), id='regular year February'),
    pytest.param(date(2020, 2, 29), (date(2020, 2, 1), date(2020, 2, 29)), id='leap year February'),
])
def test_month_range(today, expected):
    assert charts.month_range(today) == expected
