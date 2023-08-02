import pytest

from juniorguru.models.sync import Sync, SyncCommand

from testing_utils import prepare_test_db


NS_IN_MIN = 60000000000


@pytest.fixture
def test_db():
    yield from prepare_test_db([Sync])


def test_start_flushes_on_different_id(test_db):
    sync = Sync.start(123)
    sync.command_start("dogs", 0)
    sync.command_end("dogs", 5 * NS_IN_MIN)
    sync = Sync.start(456)
    sync.command_start("cats", 5 * NS_IN_MIN)
    sync.command_end("cats", 10 * NS_IN_MIN)

    assert Sync.select().count() == 1
    assert SyncCommand.select().count() == 1


def test_start_continues_on_the_same_id(test_db):
    sync = Sync.start(123)
    sync.command_start("dogs", 0)
    sync.command_end("dogs", 5 * NS_IN_MIN)
    sync = Sync.start(123)
    sync.command_start("cats", 5 * NS_IN_MIN)
    sync.command_end("cats", 10 * NS_IN_MIN)

    assert Sync.select().count() == 1
    assert SyncCommand.select().count() == 2


def test_count_commands(test_db):
    sync = Sync.start(123)
    sync.command_start("dogs", 0)
    sync.command_end("dogs", 5 * NS_IN_MIN)
    sync.command_start("cats", 5 * NS_IN_MIN)
    sync.command_end("cats", 15 * NS_IN_MIN)

    assert sync.count_commands() == 2


def test_times_min(test_db):
    sync = Sync.start(123)
    sync.command_start("dogs", 0)
    sync.command_end("dogs", 5 * NS_IN_MIN)
    sync.command_start("cats", 5 * NS_IN_MIN)
    sync.command_end("cats", 15 * NS_IN_MIN)
    sync.command_start("cows", 15 * NS_IN_MIN)
    sync.command_end("cows", 30 * NS_IN_MIN)

    assert sync.times_min() == dict(cows=15, cats=10, dogs=5)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("dogs", True),
        ("cats", False),
    ],
)
def test_is_command_seen(test_db, name, expected):
    sync = Sync.start(123)
    sync.command_start("dogs", 0)
    sync.command_end("dogs", 5 * NS_IN_MIN)

    assert sync.is_command_seen(name) is expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("dogs", False),
        ("cats", True),
    ],
)
def test_is_command_unseen(test_db, name, expected):
    sync = Sync.start(123)
    sync.command_start("dogs", 0)
    sync.command_end("dogs", 5 * NS_IN_MIN)

    assert sync.is_command_unseen(name) is expected
