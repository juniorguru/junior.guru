from dataclasses import dataclass
from datetime import date
from operator import attrgetter

import pytest

from jg.coop.lib import charts


@dataclass
class DailyItem:
    day: date
    listed: int
    dropped: int


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


@pytest.mark.parametrize(
    "today, expected",
    [
        pytest.param(
            date(2021, 8, 30),
            (date(2020, 8, 30), date(2021, 8, 30)),
            id="random specific date",
        ),
        pytest.param(
            date(2021, 12, 31),
            (date(2020, 12, 31), date(2021, 12, 31)),
            id="last day of the year",
        ),
        pytest.param(
            date(2020, 2, 29), (date(2019, 2, 28), date(2020, 2, 29)), id="leap year #1"
        ),
        pytest.param(
            date(2021, 2, 28), (date(2020, 2, 28), date(2021, 2, 28)), id="leap year #2"
        ),
    ],
)
def test_ttm_range(today, expected):
    assert charts.ttm_range(today) == expected


@pytest.mark.parametrize(
    "today, expected",
    [
        pytest.param(
            date(2021, 8, 30),
            (date(2021, 8, 1), date(2021, 8, 31)),
            id="random specific date",
        ),
        pytest.param(
            date(2021, 2, 28),
            (date(2021, 2, 1), date(2021, 2, 28)),
            id="regular year February",
        ),
        pytest.param(
            date(2020, 2, 29),
            (date(2020, 2, 1), date(2020, 2, 29)),
            id="leap year February",
        ),
    ],
)
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
        (date(2020, 2, 14), "Valentýn"),
        (date(2020, 4, 13), "Velikonoce"),
    ]
    expected_year_x = 0
    expected_valentyn_x = 1
    expected_velikonoce_x = 3

    assert charts.milestones(months, milestones) == {
        "common": {"drawTime": "beforeDatasetsDraw"},
        "annotations": {
            "2020": {
                "xMin": expected_year_x,
                "xMax": expected_year_x,
                **charts.ANNOTATION_YEAR_OPTIONS,
            },
            "valentyn-label": {
                "content": ["Valentýn"],
                "xValue": expected_valentyn_x,
                **charts.ANNOTATION_LABEL_OPTIONS,
            },
            "valentyn-line": {
                "xMin": expected_valentyn_x,
                "xMax": expected_valentyn_x,
                **charts.ANNOTATION_LINE_OPTIONS,
            },
            "velikonoce-label": {
                "content": ["Velikonoce"],
                "xValue": expected_velikonoce_x,
                **charts.ANNOTATION_LABEL_OPTIONS,
            },
            "velikonoce-line": {
                "xMin": expected_velikonoce_x,
                "xMax": expected_velikonoce_x,
                **charts.ANNOTATION_LINE_OPTIONS,
            },
        },
    }


def test_milestones_skips_milestones_out_of_range():
    months = [date(2020, 4, 30)]
    milestones = [(date(2020, 4, 13), "Velikonoce"), (date(2020, 12, 24), "Vánoce")]
    result = charts.milestones(months, milestones)

    assert set(result["annotations"].keys()) == {"velikonoce-label", "velikonoce-line"}


def test_milestones_handles_years_correctly():
    months = [date(2019, 4, 30), date(2020, 4, 30), date(2021, 4, 30)]
    milestones = [(date(2020, 4, 13), "Velikonoce")]
    result = charts.milestones(months, milestones)

    assert result["annotations"]["velikonoce-label"]["xValue"] == 1
    assert result["annotations"]["velikonoce-line"]["xMin"] == 1
    assert result["annotations"]["velikonoce-line"]["xMax"] == 1


def test_milestones_label_splits_by_whitespace():
    months = [date(2020, 4, 30)]
    milestones = [(date(2020, 4, 13), "Velikonoční pondělí")]
    result = charts.milestones(months, milestones)
    annotation = result["annotations"]["velikonocni-pondeli-label"]

    assert annotation["content"] == ["Velikonoční", "pondělí"]


def test_milestones_label_respects_nbsp():
    months = [date(2020, 4, 30)]
    milestones = [(date(2020, 4, 13), "Velikonoční pondělí")]
    result = charts.milestones(months, milestones)
    annotation = result["annotations"]["velikonocni-pondeli-label"]

    assert annotation["content"] == ["Velikonoční pondělí"]


@pytest.mark.parametrize(
    "day, expected",
    [
        pytest.param(
            date(2026, 5, 4),
            date(2026, 5, 31),
            id="regular month",
        ),
        pytest.param(
            date(2021, 2, 10),
            date(2021, 2, 28),
            id="short February",
        ),
        pytest.param(
            date(2020, 2, 10),
            date(2020, 2, 29),
            id="long February",
        ),
    ],
)
def test_month_end(day, expected):
    assert charts.month_end(day) == expected


def test_group_by_month_end():
    items = [
        DailyItem(day=date(2026, 5, 4), listed=11, dropped=21),
        DailyItem(day=date(2026, 5, 11), listed=13, dropped=23),
        DailyItem(day=date(2026, 6, 1), listed=15, dropped=25),
    ]

    mapping = charts.group_by_month_end(items, attrgetter("day"))

    assert set(mapping.keys()) == {date(2026, 5, 31), date(2026, 6, 30)}
    assert [item.listed for item in mapping[date(2026, 5, 31)]] == [11, 13]
    assert [item.listed for item in mapping[date(2026, 6, 30)]] == [15]


@pytest.mark.parametrize(
    "values, expected",
    [
        pytest.param([10, 11, 12], 11, id="three values"),
        pytest.param([10, 11], 10, id="bankers rounding"),
    ],
)
def test_average_round(values, expected):
    assert charts.average_round(values) == expected


def test_per_month_aggregate_breakdown():
    items = [
        DailyItem(day=date(2026, 5, 4), listed=10, dropped=20),
        DailyItem(day=date(2026, 5, 11), listed=12, dropped=24),
        DailyItem(day=date(2026, 6, 1), listed=20, dropped=40),
    ]

    months, data = charts.per_month_aggregate_breakdown(
        items,
        day_fn=attrgetter("day"),
        value_fns={
            "listed": attrgetter("listed"),
            "dropped": attrgetter("dropped"),
        },
        aggregate_fn=charts.average_round,
    )

    assert months == [date(2026, 5, 31), date(2026, 6, 30)]
    assert data == {"listed": [11, 20], "dropped": [22, 40]}


def test_per_month_aggregate_breakdown_empty_input():
    months, data = charts.per_month_aggregate_breakdown(
        [],
        day_fn=attrgetter("day"),
        value_fns={
            "listed": attrgetter("listed"),
            "dropped": attrgetter("dropped"),
        },
        aggregate_fn=charts.average_round,
    )

    assert months == []
    assert data == {"listed": [], "dropped": []}


@pytest.mark.parametrize(
    "values, previous_values, expected",
    [
        pytest.param([120], [100], [20.0], id="growth"),
        pytest.param([80], [100], [-20.0], id="decline"),
        pytest.param([100], [100], [0.0], id="flat"),
        pytest.param([None], [100], [None], id="missing current value"),
        pytest.param([120], [None], [None], id="missing previous value"),
        pytest.param([120], [0], [None], id="zero previous value avoids division"),
        pytest.param(
            [110, 90, 200],
            [100, 100, 100],
            [10.0, -10.0, 100.0],
            id="multiple values",
        ),
        pytest.param([], [], [], id="empty"),
    ],
)
def test_growth_ptc(values, previous_values, expected):
    assert charts.growth_ptc(values, previous_values) == expected
