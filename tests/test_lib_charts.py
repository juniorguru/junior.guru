from datetime import date

import pytest

from juniorguru.lib import charts


def test_months():
    assert list(charts.months(date(2020, 1, 15), date(2020, 8, 28))) == [
        date(2020, 1, 31),
        date(2020, 2, 29),
        date(2020, 3, 31),
        date(2020, 4, 30),
        date(2020, 5, 31),
        date(2020, 6, 30),
        date(2020, 7, 31),
        date(2020, 8, 28),
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


def test_annotations():
    months = [
        date(2020, 1, 31),
        date(2020, 2, 29),
        date(2020, 3, 31),
        date(2020, 4, 30),
        date(2020, 5, 31),
    ]
    milestones = [
        (date(2020, 2, 14), 'Valentýn'),
        (date(2020, 4, 13), 'Velikonoce'),
    ]
    expected_year_x = 0
    expected_valentyn_x = 1
    expected_velikonoce_x = 3

    assert charts.annotations(months, milestones) == {
        'common': {'drawTime': 'beforeDatasetsDraw'},
        'annotations': {
            '2020': {
                'xMin': expected_year_x,
                'xMax': expected_year_x,
                **charts.ANNOTATION_YEAR_OPTIONS,
            },
            'valentyn-label': {
                'content': ['Valentýn'],
                'xValue': expected_valentyn_x,
                **charts.ANNOTATION_LABEL_OPTIONS,
            },
            'valentyn-line': {
                'xMin': expected_valentyn_x,
                'xMax': expected_valentyn_x,
                **charts.ANNOTATION_LINE_OPTIONS,
            },
            'velikonoce-label': {
                'content': ['Velikonoce'],
                'xValue': expected_velikonoce_x,
                **charts.ANNOTATION_LABEL_OPTIONS,
            },
            'velikonoce-line': {
                'xMin': expected_velikonoce_x,
                'xMax': expected_velikonoce_x,
                **charts.ANNOTATION_LINE_OPTIONS,
            },
        }
    }


def test_annotations_skips_milestones_out_of_range():
    months = [date(2020, 4, 30)]
    milestones = [(date(2020, 4, 13), 'Velikonoce'),
                  (date(2020, 12, 24), 'Vánoce')]
    result = charts.annotations(months, milestones)

    assert set(result['annotations'].keys()) == {'velikonoce-label', 'velikonoce-line'}


def test_annotations_handles_years_correctly():
    months = [date(2019, 4, 30),
              date(2020, 4, 30),
              date(2021, 4, 30)]
    milestones = [(date(2020, 4, 13), 'Velikonoce')]
    result = charts.annotations(months, milestones)

    assert result['annotations']['velikonoce-label']['xValue'] == 1
    assert result['annotations']['velikonoce-line']['xMin'] == 1
    assert result['annotations']['velikonoce-line']['xMax'] == 1


def test_annotations_label_splits_by_whitespace():
    months = [date(2020, 4, 30)]
    milestones = [(date(2020, 4, 13), 'Velikonoční pondělí')]
    result = charts.annotations(months, milestones)
    annotation = result['annotations']['velikonocni-pondeli-label']

    assert annotation['content'] == ['Velikonoční', 'pondělí']


def test_annotations_label_respects_nbsp():
    months = [date(2020, 4, 30)]
    milestones = [(date(2020, 4, 13), 'Velikonoční pondělí')]
    result = charts.annotations(months, milestones)
    annotation = result['annotations']['velikonocni-pondeli-label']

    assert annotation['content'] == ['Velikonoční pondělí']
