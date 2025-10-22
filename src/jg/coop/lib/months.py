from datetime import date, timedelta


def this_month(today: date) -> date:
    return today.replace(day=1)


def prev_month(today: date) -> date:
    return (this_month(today) - timedelta(days=1)).replace(day=1)


def prev_prev_month(today: date) -> date:
    return (prev_month(today) - timedelta(days=1)).replace(day=1)
