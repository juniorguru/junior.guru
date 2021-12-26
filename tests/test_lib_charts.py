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
        # first_transaction.happened_on

        # while point_date <= to_date:
        #     point_date = point_date.replace(day=calendar.monthrange(point_date.year, point_date.month)[1])
        #     yield point_date
        #     point_date = point_date.replace(day=1)


# @pytest.mark.parametrize('today, expected', [
#     pytest.param(date(2021, 8, 30), (date(2020, 8, 31), date(2021, 8, 30)), id='random specific date'),
#     pytest.param(date(2021, 12, 31), (date(2021, 1, 1), date(2021, 12, 31)), id='last day of the year'),
#     pytest.param(date(2020, 2, 29), (date(2019, 3, 1), date(2020, 2, 29)), id='leap year #1'),
#     pytest.param(date(2021, 2, 28), (date(2020, 2, 29), date(2021, 2, 28)), id='leap year #2'),
# ])
# def test_ttm_range(today, expected):
#     assert charts.ttm_range(today) == expected


@pytest.mark.parametrize('today, expected', [
    pytest.param(date(2021, 8, 30), (date(2021, 8, 1), date(2021, 8, 31)), id='random specific date'),
    pytest.param(date(2021, 2, 28), (date(2021, 2, 1), date(2021, 2, 28)), id='regular year February'),
    pytest.param(date(2020, 2, 29), (date(2020, 2, 1), date(2020, 2, 29)), id='leap year February'),
])
def test_month_range(today, expected):
    assert charts.month_range(today) == expected


# @pytest.mark.parametrize('range, expected', [
#     ((date(2020, 1, 1), date(2020, 12, 31)),
#      [date(2020, 1, 31), date(2020, 2, 29), date(2020, 3, 31),
#       date(2020, 4, 30), date(2020, 5, 31), date(2020, 6, 30),
#       date(2020, 7, 31), date(2020, 8, 31), date(2020, 9, 30),
#       date(2020, 10, 31), date(2020, 11, 30), date(2020, 12, 31)]),
#     ((date(2020, 8, 16), date(2021, 8, 15)),
#      [date(2020, 9, 15), date(2020, 10, 15), date(2020, 11, 15),
#       date(2020, 12, 15), date(2021, 1, 15), date(2021, 2, 15),
#       date(2021, 3, 15), date(2021, 4, 15), date(2021, 5, 15),
#       date(2021, 6, 15), date(2021, 7, 15), date(2021, 8, 15)]),
# ])
# def test_data_points(range, expected):
#     assert charts.data_points(range) == expected


def test_charts_ranges():
    assert charts.charts_ranges(date(2021, 8, 30)) == {
        'today': (date(2020, 8, 30), date(2021, 8, 30)),
        '2020': (date(2020, 1, 1), date(2020, 12, 31)),
    }


def test_charts_ranges_goes_as_far_as_2020():
    assert charts.charts_ranges(date(2025, 8, 30)) == {
        'today': (date(2024, 8, 30), date(2025, 8, 30)),
        '2024': (date(2024, 1, 1), date(2024, 12, 31)),
        '2023': (date(2023, 1, 1), date(2023, 12, 31)),
        '2022': (date(2022, 1, 1), date(2022, 12, 31)),
        '2021': (date(2021, 1, 1), date(2021, 12, 31)),
        '2020': (date(2020, 1, 1), date(2020, 12, 31)),
    }
