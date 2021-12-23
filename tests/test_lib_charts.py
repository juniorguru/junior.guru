from datetime import date

import pytest

from juniorguru.lib import charts


@pytest.mark.parametrize('today, expected', [
    (date(2021, 8, 30), [date(2020, 9, 30), date(2020, 10, 31), date(2020, 11, 30),
                         date(2020, 12, 31), date(2021, 1, 31), date(2021, 2, 28),
                         date(2021, 3, 31), date(2021, 4, 30), date(2021, 5, 31),
                         date(2021, 6, 30), date(2021, 7, 31), date(2021, 8, 31)]),
    (date(2020, 3, 31), [date(2019, 4, 30), date(2019, 5, 31), date(2019, 6, 30),
                         date(2019, 7, 31), date(2019, 8, 31), date(2019, 9, 30),
                         date(2019, 10, 31), date(2019, 11, 30), date(2019, 12, 31),
                         date(2020, 1, 31), date(2020, 2, 29), date(2020, 3, 31)]),
])
def test_data_points(today, expected):
    assert charts.data_points(today) == expected


def test_ranges():
    assert charts.ranges(date(2021, 8, 30)) == {'today': charts.data_points(date(2021, 8, 30)),
                                                '2020': charts.data_points(date(2020, 12, 31))}


def test_ranges_goes_as_far_as_2020():
    assert charts.ranges(date(2025, 8, 30)) == {'today': charts.data_points(date(2025, 8, 30)),
                                                '2024': charts.data_points(date(2024, 12, 31)),
                                                '2023': charts.data_points(date(2023, 12, 31)),
                                                '2022': charts.data_points(date(2022, 12, 31)),
                                                '2021': charts.data_points(date(2021, 12, 31)),
                                                '2020': charts.data_points(date(2020, 12, 31))}
