from datetime import date

import pytest

from juniorguru.fetch.lib import google_analytics


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
            'rows': [[
                {'dimensions': ['20200620'], 'metrics': [{'values': ['1102']}]},
                {'dimensions': ['20200621'], 'metrics': [{'values': ['1037']}]},
                {'dimensions': ['20200622'], 'metrics': [{'values': ['4583']}]},
                {'dimensions': ['20200623'], 'metrics': [{'values': ['3292']}]},
                {'dimensions': ['20200624'], 'metrics': [{'values': ['1833']}]},
                {'dimensions': ['20200625'], 'metrics': [{'values': ['1227']}]},
            ] for _ in range(21)],
            'totals': [
                {'values': ['282324']},
            ],
            'rowCount': 126,
            'minimums': [{'values': ['1037']}],
            'maximums': [{'values': ['4583']}],
            'isDataGolden': True
        }
    }) == (282324 / (126 / 30))


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


def test_per_url_locations_report_to_dict():
    assert google_analytics.per_url_locations_report_to_dict({
        'columnHeader': {
            'dimensions': ['ga:eventLabel', 'ga:region'],
            'metricHeader': {
                'metricHeaderEntries': [
                    {'name': 'ga:pageviews', 'type': 'INTEGER'}
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
                    'dimensions': ['https://junior.guru/jobs/xyz1/', 'Brno'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/', 'Praha'],
                    'metrics': [{'values': ['2']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/', 'Brno'],
                    'metrics': [{'values': ['2']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/', 'Pardubice'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz1/', 'Brno'],
                    'metrics': [{'values': ['5']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/', 'Ostrava'],
                    'metrics': [{'values': ['1']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/', 'Ostrava'],
                    'metrics': [{'values': ['4']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/', 'Praha'],
                    'metrics': [{'values': ['6']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/', 'Vysočina'],
                    'metrics': [{'values': ['4']}]
                },
                {
                    'dimensions': ['https://junior.guru/jobs/xyz2/', 'Zlín'],
                    'metrics': [{'values': ['2']}]
                }
            ],
            'totals': [{'values': ['28']}]
        }
    }) == {
        'https://junior.guru/jobs/xyz1/': {
            'Brno': 8,
            'Praha': 2,
            'Pardubice': 1,
        },
        'https://junior.guru/jobs/xyz2/': {
            'Praha': 6,
            'Ostrava': 5,
            'Vysočina': 4,
            'Zlín': 2,
        },
    }
