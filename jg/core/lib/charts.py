import calendar
import itertools
from datetime import date, timedelta
from functools import cache
from numbers import Number
from typing import Callable, Generator, Iterable

from slugify import slugify


ANNOTATION_LABEL_OPTIONS = {
    "type": "label",
    "color": "#aaa",
    "backgroundColor": "white",
    "borderRadius": 3,
    "padding": 3,
    "position": {"x": "start", "y": "start"},
    "textAlign": "left",
    "xAdjust": 1,
    "yAdjust": 5,
    "z": 2,
}

ANNOTATION_LINE_OPTIONS = {
    "type": "line",
    "borderColor": "#bbb",
    "borderWidth": 1,
}

ANNOTATION_YEAR_OPTIONS = {
    "type": "line",
    "borderColor": "#666",
    "borderWidth": 1,
    "borderDash": [3, 3],
    "z": 1,
}


@cache
def months(from_date: date, to_date: date) -> list[date]:
    return list(generate_months(from_date, to_date))


def generate_months(from_date: date, to_date: date) -> Generator[date, None, None]:
    d = from_date
    while d <= to_date:
        last_date_of_month = d.replace(day=calendar.monthrange(d.year, d.month)[1])
        yield min(last_date_of_month, to_date)
        d = last_date_of_month + timedelta(days=1)


def labels(months: list[date]) -> list[str]:
    return [f"{month:%Y-%m}" for month in months]


def per_month(fn_returning_numbers: Callable, months: Iterable[date]) -> list[Number]:
    return [fn_returning_numbers(month) for month in months]


def per_month_breakdown(
    fn_returning_breakdowns: Callable, months: Iterable[date]
) -> dict[str, list[Number]]:
    breakdowns = [fn_returning_breakdowns(month) for month in months]
    categories = set(
        itertools.chain.from_iterable(breakdown.keys() for breakdown in breakdowns)
    )
    return {
        category: [breakdown.get(category) for breakdown in breakdowns]
        for category in categories
    }


@cache
def ttm_range(date: date) -> tuple[date, date]:
    try:
        return (date.replace(year=date.year - 1), date)
    except ValueError:  # 29th February
        return (date.replace(year=date.year - 1, day=date.day - 1), date)


@cache
def month_range(date: date) -> tuple[date, date]:
    return (
        date.replace(day=1),
        date.replace(day=calendar.monthrange(date.year, date.month)[1]),
    )


def milestones(months: list[date], milestones: list[tuple[date, str]]) -> dict:
    annotations = {
        f"{month.year}": {
            "xMin": x,
            "xMax": x,
            **ANNOTATION_YEAR_OPTIONS,
        }
        for x, month in enumerate(months)
        if month.month == 1  # January
    }
    for milestone_date, milestone_name in dict(milestones).items():
        name = slugify(milestone_name)
        try:
            x = [
                index
                for index, month in enumerate(months)
                if (
                    month.year == milestone_date.year
                    and month.month == milestone_date.month
                )
            ][0]
        except IndexError:
            continue
        else:
            annotations[f"{name}-label"] = {
                "content": milestone_name.split(" "),
                "xValue": x,
                **ANNOTATION_LABEL_OPTIONS,
            }
            annotations[f"{name}-line"] = {
                "xMin": x,
                "xMax": x,
                **ANNOTATION_LINE_OPTIONS,
            }
    return {
        "common": {"drawTime": "beforeDatasetsDraw"},
        "annotations": annotations,
    }


@cache
def previous_month(month: date) -> date:
    return month.replace(day=1) - timedelta(days=1)


@cache
def next_month(month: date) -> date:
    return (month.replace(day=1) + timedelta(days=32)).replace(day=1)
