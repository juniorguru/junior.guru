from datetime import date, datetime, time

import pytest
from peewee import OperationalError

from juniorguru.models import base as models_base
from juniorguru.jobs.items import Job


@pytest.fixture
def db():
    class DummyDB():
        def __init__(self):
            self.entered = 0
            self.exited = 0

        def __enter__(self):
            self.entered += 1

        def __exit__(self, *args, **kwargs):
            self.exited += 1

    return DummyDB()


@pytest.fixture
def stats():
    class DummyStats():
        def __init__(self):
            self.values = {}

        def inc_value(self, name):
            self.values.setdefault(name, 0)
            self.values[name] += 1

    return DummyStats()


@pytest.mark.parametrize('o,expected', [
    ([1, 2, 3], '[1, 2, 3]'),
    (datetime(2020, 4, 30, 14, 35, 10), '"2020-04-30T14:35:10"'),
    (date(2020, 4, 30), '"2020-04-30"'),
    (time(14, 35, 10), '"14:35:10"'),
    ([1, 2, datetime(2020, 4, 30, 14, 35, 10)], '[1, 2, "2020-04-30T14:35:10"]'),
    ({'posted_at': datetime(2020, 4, 30, 14, 35, 10)}, '{"posted_at": "2020-04-30T14:35:10"}'),
    ({1, 2, 3}, '[1, 2, 3]'),
    (frozenset([1, 2, 3]), '[1, 2, 3]'),
])
def test_json_dumps(o, expected):
    assert models_base.json_dumps(o) == expected


def test_json_dumps_item():
    job = Job(posted_at=datetime(2020, 4, 30, 14, 35, 10),
              title='Junior developer',
              employment_types=frozenset(['full-time']))

    assert models_base.json_dumps(job) == ('{'
        '"posted_at": "2020-04-30T14:35:10", '
        '"title": "Junior developer", '
        '"employment_types": ["full-time"]'
    '}')


def test_retry_when_db_locked(db, stats):
    def operation():
        if stats.values.get('database/locked_retries', 0) < 5:
            raise OperationalError('database is locked')
        return 42

    _ = models_base.retry_when_db_locked(db, operation, stats=stats, wait_sec=0)

    assert _ == 42
    assert db.entered == 6
    assert db.exited == 6
    assert stats.values == {'database/locked_retries': 5}


def test_retry_when_db_locked_raises(db, stats):
    def operation():
        raise OperationalError('database is locked')

    with pytest.raises(OperationalError):
        models_base.retry_when_db_locked(db, operation, stats=stats, wait_sec=0)

    assert db.entered == 10
    assert db.exited == 10
    assert stats.values == {'database/locked_retries': 10, 'database/uncaught_errors': 1}
