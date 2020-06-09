import hashlib
from datetime import date

import pytest

from juniorguru.fetch import fetch_metrics


@pytest.mark.parametrize('today,expected_start,expected_end', [
    (date(2020, 6, 9), date(2019, 12, 1), date(2020, 5, 31)),
    (date(2020, 5, 31), date(2019, 11, 1), date(2020, 4, 30)),
])
def test_get_range_months(today, expected_start, expected_end):
    expected_range = (expected_start, expected_end)

    assert fetch_metrics.get_range_months(6, today=today) == expected_range


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
