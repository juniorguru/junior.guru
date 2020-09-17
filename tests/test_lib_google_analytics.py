import math
from datetime import date, timedelta

import pytest

from juniorguru.lib import google_analytics


@pytest.mark.parametrize('today,expected_start,expected_end', [
    (date(2020, 6, 9), date(2019, 1, 1), date(2020, 6, 8)),
    (date(2020, 5, 31), date(2019, 1, 1), date(2020, 5, 30)),
])
def test_get_daily_date_range(today, expected_start, expected_end):
    expected = (expected_start, expected_end)

    assert google_analytics.get_daily_date_range(today=today) == expected


@pytest.mark.parametrize('today,months,expected_start,expected_end', [
    (date(2020, 6, 9), 6, date(2019, 12, 8), date(2020, 6, 8)),
])
def test_get_daily_date_range_start_months_ago(today, months, expected_start, expected_end):
    expected = (expected_start, expected_end)

    assert google_analytics.get_daily_date_range(today=today,
                                                 start_months_ago=months) == expected


def test_calc_avg_monthly_values():
    init_date = date(2020, 6, 14)
    assert google_analytics.calc_avg_monthly_values({
        'columnHeader': {
            'dimensions': ['ga:date'],
            'metricHeader': {
                'metricHeaderEntries': [
                    {'name': 'ga:users', 'type': 'INTEGER'}
                ]
            }
        },
        'data': {
            'rows': [
                {
                    'dimensions': [(init_date + timedelta(days=i)).strftime('%Y%m%d')],
                    'metrics': [{'values': [str(1000 + i)]}],
                }
                for i in range(65)
            ],
            'totals': [
                {'values': ['67080']},
            ],
            'rowCount': 65,
            'minimums': [{'values': ['1000']}],
            'maximums': [{'values': ['1064']}],
            'isDataGolden': True
        }
    }) == math.ceil(67080 / (65 / 30))


def test_calc_avg_monthly_values_sparse_data():
    init_date = date(2020, 6, 14)
    assert google_analytics.calc_avg_monthly_values({
        'columnHeader': {
            'dimensions': ['ga:date'],
            'metricHeader': {
                'metricHeaderEntries': [
                    {'name': 'ga:users', 'type': 'INTEGER'}
                ]
            }
        },
        'data': {
            'rows': [
                {
                    'dimensions': [(init_date + timedelta(days=i)).strftime('%Y%m%d')],
                    'metrics': [{'values': [str(1000 + i)]}],
                }
                for i in range(2, 65, 3)
            ],
            'totals': [
                {'values': ['21672']},
            ],
            'rowCount': 21,
            'minimums': [{'values': ['1000']}],
            'maximums': [{'values': ['1063']}],
            'isDataGolden': True
        }
    }) == math.ceil(21672 / (61 / 30))  # 2020-08-15 - 2020-06-16 = 61 days


def test_per_url_report_to_dict():
    assert google_analytics.per_url_report_to_dict({
        'columnHeader': {
            'dimensions': ['ga:eventLabel'],
            'metricHeader': {
                'metricHeaderEntries': [
                    {'name': 'ga:uniqueEvents', 'type': 'INTEGER'}
                ]
            }
        },
        'data': {
            'isDataGolden': True,
            'maximums': [{'values': ['6']}],
            'minimums': [{'values': ['1']}],
            'rowCount': 10,
            'rows': [
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/'],
                    'metrics': [{'values': ['2']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz3/'],
                    'metrics': [{'values': ['2']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz4/'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz5/'],
                    'metrics': [{'values': ['5']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz6/'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz7/'],
                    'metrics': [{'values': ['4']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz8/'],
                    'metrics': [{'values': ['6']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz9/'],
                    'metrics': [{'values': ['4']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz0/'],
                    'metrics': [{'values': ['2']}]
                }
            ],
            'totals': [{'values': ['28']}]
        }
    }) == {
        'https://junior.guru/jobs/xyz1/': 1,
        'https://junior.guru/jobs/xyz2/': 2,
        'https://junior.guru/jobs/xyz3/': 2,
        'https://junior.guru/jobs/xyz4/': 1,
        'https://junior.guru/jobs/xyz5/': 5,
        'https://junior.guru/jobs/xyz6/': 1,
        'https://junior.guru/jobs/xyz7/': 4,
        'https://junior.guru/jobs/xyz8/': 6,
        'https://junior.guru/jobs/xyz9/': 4,
        'https://junior.guru/jobs/xyz0/': 2,
    }


def test_per_date_report_to_dict():
    init_date = date(2020, 6, 14)
    assert google_analytics.per_date_report_to_dict({
        'columnHeader': {
            'dimensions': ['ga:date'],
            'metricHeader': {
                'metricHeaderEntries': [
                    {'name': 'ga:users', 'type': 'INTEGER'}
                ]
            }
        },
        'data': {
            'rows': [
                {
                    'dimensions': [(init_date + timedelta(days=i)).strftime('%Y%m%d')],
                    'metrics': [{'values': [str(1000 + i)]}],
                }
                for i in range(9)
            ],
            'totals': [
                {'values': ['9036']},
            ],
            'rowCount': 9,
            'minimums': [{'values': ['1000']}],
            'maximums': [{'values': ['1008']}],
            'isDataGolden': True
        }
    }) == {
        date(2020, 6, 14): 1000,
        date(2020, 6, 15): 1001,
        date(2020, 6, 16): 1002,
        date(2020, 6, 17): 1003,
        date(2020, 6, 18): 1004,
        date(2020, 6, 19): 1005,
        date(2020, 6, 20): 1006,
        date(2020, 6, 21): 1007,
        date(2020, 6, 22): 1008,
    }


def test_per_url_report_to_dict_trims_fbclid():
    assert google_analytics.per_url_report_to_dict({
        'columnHeader': {
            'dimensions': ['ga:eventLabel'],
            'metricHeader': {
                'metricHeaderEntries': [
                    {'name': 'ga:uniqueEvents', 'type': 'INTEGER'}
                ]
            }
        },
        'data': {
            'isDataGolden': True,
            'maximums': [{'values': ['5']}],
            'minimums': [{'values': ['1']}],
            'rowCount': 10,
            'rows': [
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/?fbclid=IwAR0tiKUPuUlwlJQmyrMMJomD3wgmhutiSOIkCREJ_lZYVONmyK68TkXxfSc'],
                    'metrics': [{'values': ['2']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/?fbclid=IwAR2Dx61q63a5_5Rpnk7-DMme0pIS0tg6iEMx_ia6sJjO5rp2dmk_ExfTjlo'],
                    'metrics': [{'values': ['2']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz3/'],
                    'metrics': [{'values': ['5']}]
                },
            ],
            'totals': [{'values': ['11']}]
        }
    }) == {
        'https://junior.guru/jobs/xyz1/': 5,
        'https://junior.guru/jobs/xyz2/': 1,
        'https://junior.guru/jobs/xyz3/': 5,
    }
