import hashlib
from datetime import date

import pytest

from juniorguru.fetch import fetch_metrics


@pytest.mark.parametrize('today,expected_start,expected_end', [
    (date(2020, 6, 9), date(2019, 12, 1), date(2020, 5, 31)),
    (date(2020, 5, 31), date(2019, 11, 1), date(2020, 4, 30)),
])
def test_get_date_range(today, expected_start, expected_end):
    expected = (expected_start, expected_end)

    assert fetch_metrics.get_date_range(6, today=today) == expected


def test_calc_avg_monthly_values():
    assert fetch_metrics.calc_avg_monthly_values({
        'reports': [
            {
                'columnHeader': {
                    'dimensions': ['ga:month'],
                    'metricHeader': {
                        'metricHeaderEntries': [
                            {'name': 'ga:users', 'type': 'INTEGER'}
                        ]
                    }
                },
                'data': {
                    'rows': [
                        {'dimensions': ['01'], 'metrics': [{'values': ['1102']}]},
                        {'dimensions': ['02'], 'metrics': [{'values': ['1037']}]},
                        {'dimensions': ['03'], 'metrics': [{'values': ['4583']}]},
                        {'dimensions': ['04'], 'metrics': [{'values': ['3292']}]},
                        {'dimensions': ['05'], 'metrics': [{'values': ['1833']}]},
                        {'dimensions': ['12'], 'metrics': [{'values': ['1227']}]},
                    ],
                    'totals': [
                        {'values': ['13074']},
                    ],
                    'rowCount': 6,
                    'minimums': [{'values': ['1037']}],
                    'maximums': [{'values': ['4583']}],
                    'isDataGolden': True
                }
            }
        ]
    }) == (13074 / 6)


@pytest.mark.parametrize('metric,expected', [
    ('ga:users', 10745 / 4),
    ('ga:pageviews', 30320 / 4),
])
@pytest.mark.skip
def test_calc_avg_monthly_values_multiple_metrics(metric, expected):
    assert fetch_metrics.calc_avg_monthly_values({
        'reports': [
            {
                'columnHeader': {
                    'dimensions': ['ga:month'],
                    'metricHeader': {
                        'metricHeaderEntries': [
                            {'name': 'ga:users', 'type': 'INTEGER'},
                            {'name': 'ga:pageviews', 'type': 'INTEGER'},
                        ]
                    }
                },
                'data': {
                    'rows': [
                        {'dimensions': ['02'], 'metrics': [{'values': ['1037', '3281']}]},
                        {'dimensions': ['03'], 'metrics': [{'values': ['4583', '10651']}]},
                        {'dimensions': ['04'], 'metrics': [{'values': ['3292', '9679']}]},
                        {'dimensions': ['05'], 'metrics': [{'values': ['1833', '6709']}]}
                    ],
                    'totals': [{'values': ['10745', '30320']}],
                    'rowCount': 4,
                    'minimums': [{'values': ['1037', '3281']}],
                    'maximums': [{'values': ['4583', '10651']}],
                    'isDataGolden': True
                }
            }
        ]
    }, metric) == expected


def test_events_data_to_dict():
    assert fetch_metrics.events_data_to_dict({
        'reports': [
            {
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
            }
        ]
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
