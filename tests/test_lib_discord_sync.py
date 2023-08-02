from functools import wraps

from juniorguru.lib import discord_sync
from juniorguru.models.base import SqliteDatabase


def test_get_import_path():
    def sample_fn():
        pass

    assert discord_sync.get_import_path(sample_fn) == (
        "test_lib_discord_sync" ".test_get_import_path" ".<locals>" ".sample_fn"
    )


def test_get_import_path_async():
    async def sample_fn():
        pass

    assert discord_sync.get_import_path(sample_fn) == (
        "test_lib_discord_sync" ".test_get_import_path_async" ".<locals>" ".sample_fn"
    )


def test_get_import_path_with_decorator():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @decorator
    def sample_fn():
        pass

    assert hasattr(sample_fn, "__wrapped__")
    assert discord_sync.get_import_path(sample_fn) == (
        "test_lib_discord_sync"
        ".test_get_import_path_with_decorator"
        ".<locals>"
        ".sample_fn"
    )


def test_get_import_path_with_db_connection_decorator():
    db = SqliteDatabase(":memory:")

    @db.connection_context()
    def sample_fn():
        pass

    assert hasattr(sample_fn, "__wrapped__")
    assert discord_sync.get_import_path(sample_fn) == (
        "test_lib_discord_sync"
        ".test_get_import_path_with_db_connection_decorator"
        ".<locals>"
        ".sample_fn"
    )


def test_get_import_path_with_db_connection_decorator_async():
    db = SqliteDatabase(":memory:")

    @db.connection_context()
    async def sample_fn():
        pass

    assert hasattr(sample_fn, "__wrapped__")
    assert discord_sync.get_import_path(sample_fn) == (
        "test_lib_discord_sync"
        ".test_get_import_path_with_db_connection_decorator_async"
        ".<locals>"
        ".sample_fn"
    )
