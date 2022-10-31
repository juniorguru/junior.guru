import pytest
from peewee import SqliteDatabase

from juniorguru.models.sync import Sync, SyncCommand


NS_IN_MIN = 60000000000


@pytest.fixture
def db_connection():
    db = SqliteDatabase(':memory:')
    with db:
        Sync.bind(db)
        yield db
        db.drop_tables([Sync, SyncCommand])


def test_start_flushes_on_different_id(db_connection):
    sync = Sync.start(123)
    sync.command_start('dogs', 0)
    sync.command_end('dogs', 5 * NS_IN_MIN)
    sync = Sync.start(456)
    sync.command_start('cats', 5 * NS_IN_MIN)
    sync.command_end('cats', 10 * NS_IN_MIN)

    assert sync.times_min() == dict(cats=5)
    assert Sync.select().count() == 1
    assert SyncCommand.select().count() == 1


def test_start_continues_on_the_same_id(db_connection):
    sync = Sync.start(123)
    sync.command_start('dogs', 0)
    sync.command_end('dogs', 5 * NS_IN_MIN)
    sync = Sync.start(123)
    sync.command_start('cats', 5 * NS_IN_MIN)
    sync.command_end('cats', 10 * NS_IN_MIN)

    assert sync.times_min() == dict(cats=5, dogs=5)
    assert Sync.select().count() == 1
    assert SyncCommand.select().count() == 2


def test_timing(db_connection):
    sync = Sync.start(123)
    sync.command_start('dogs', 0)
    sync.command_end('dogs', 5 * NS_IN_MIN)
    sync.command_start('cats', 5 * NS_IN_MIN)
    sync.command_end('cats', 15 * NS_IN_MIN)
    sync.command_start('cows', 15 * NS_IN_MIN)
    sync.command_end('cows', 30 * NS_IN_MIN)

    assert sync.times_min() == dict(cows=15, cats=10, dogs=5)


@pytest.mark.parametrize('name, expected', [
    ('dogs', True),
    ('cats', False),
])
def test_is_command_seen(db_connection, name, expected):
    sync = Sync.start(123)
    sync.command_start('dogs', 0)
    sync.command_end('dogs', 5 * NS_IN_MIN)

    assert sync.is_command_seen(name) is expected


@pytest.mark.parametrize('name, expected', [
    ('dogs', False),
    ('cats', True),
])
def test_is_command_unseen(db_connection, name, expected):
    sync = Sync.start(123)
    sync.command_start('dogs', 0)
    sync.command_end('dogs', 5 * NS_IN_MIN)

    assert sync.is_command_unseen(name) is expected
