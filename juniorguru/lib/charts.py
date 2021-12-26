import itertools
import calendar

from datetime import timedelta


def months(from_date, to_date):
    return list(generate_months(from_date, to_date))


def generate_months(from_date, to_date):
    d = from_date
    while d <= to_date:
        last_date_of_month = d.replace(day=calendar.monthrange(d.year, d.month)[1])
        yield last_date_of_month
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
