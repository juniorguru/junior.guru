from collections import namedtuple
from datetime import datetime, date

from juniorguru.sync.meetups import is_future_event


StubEvent = namedtuple('Event', ['begin', 'categories'], defaults=dict(categories=[]))


def test_is_future_event():
    event = StubEvent(begin=datetime(2023, 7, 3, 18, 0, 0))

    assert is_future_event(event, date(2023, 7, 1)) is True


def test_is_future_event_today():
    event = StubEvent(begin=datetime(2023, 7, 3, 18, 0, 0))

    assert is_future_event(event, date(2023, 7, 3)) is True


def test_is_future_event_past():
    event = StubEvent(begin=datetime(2023, 7, 3, 18, 0, 0))

    assert is_future_event(event, date(2023, 7, 4)) is False


def test_is_future_event_tentative():
    event = StubEvent(begin=datetime(2023, 7, 3, 18, 0, 0), categories=['tentative-date'])

    assert is_future_event(event, date(2023, 7, 1)) is False
