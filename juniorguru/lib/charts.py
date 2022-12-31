import calendar
import itertools
from datetime import timedelta

from slugify import slugify


ANNOTATION_LABEL_OPTIONS = {
    'type': 'label',
    'color': '#666',
    'backgroundColor': 'white',
    'borderRadius': 3,
    'padding': 3,
    'position': {'x': 'center', 'y': 'start'},
    'yAdjust': 10,
    'z': 1,
}

ANNOTATION_LINE_OPTIONS = {
    'type': 'line',
    'borderColor': '#666',
    'borderWidth': 1,
    'borderDash': [3, 3],
}


def months(from_date, to_date):
    return list(generate_months(from_date, to_date))


def generate_months(from_date, to_date):
    d = from_date
    while d <= to_date:
        last_date_of_month = d.replace(day=calendar.monthrange(d.year, d.month)[1])
        yield min(last_date_of_month, to_date)
        d = last_date_of_month + timedelta(days=1)


def labels(months):
    return [f'{month:%Y-%m}' for month in months]


def per_month(fn_returning_numbers, months):
    return [fn_returning_numbers(month) for month in months]


def per_month_breakdown(fn_returning_breakdowns, months):
    breakdowns = [fn_returning_breakdowns(month) for month in months]
    categories = set(itertools.chain.from_iterable(breakdown.keys() for breakdown in breakdowns))
    return {category: [breakdown.get(category, 0) for breakdown in breakdowns]
            for category in categories}


def ttm_range(date):
    try:
        return (date.replace(year=date.year - 1), date)
    except ValueError:  # 29th February
        return (date.replace(year=date.year - 1, day=date.day - 1), date)


def month_range(date):
    return (date.replace(day=1), date.replace(day=calendar.monthrange(date.year, date.month)[1]))


def annotations(months, events):
    annotations = {}
    for event_date, event_name in dict(events).items():
        name = slugify(event_name)
        x = [index for index, month in enumerate(months)
             if (month.year == event_date.year and
                 month.month == event_date.month)][0]
        annotations[f'{name}-label'] = {
            'content': event_name.split(' '),
            'xValue': x,
            **ANNOTATION_LABEL_OPTIONS,
        }
        annotations[f'{name}-line'] = {
            'xMin': x,
            'xMax': x,
            **ANNOTATION_LINE_OPTIONS,
        }
    return {
        'common': {'drawTime': 'beforeDatasetsDraw'},
        'annotations': annotations,
    }
