import calendar

from datetime import timedelta, date


RANGES_BEGINNING_YEAR = 2020


def data_points(today):
    points = []
    last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    for _ in range(12):
        points.append(last_day_of_month)
        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
    return list(reversed(points))


def ranges(today):
    return dict(today=data_points(today), **{
        f'{year}': data_points(date(year, 12, 31)) for year
        in range(RANGES_BEGINNING_YEAR, today.year)
    })
