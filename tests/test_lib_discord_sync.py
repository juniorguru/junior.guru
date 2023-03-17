from functools import wraps

from peewee import SqliteDatabase

from juniorguru.lib import discord_sync


def test_get_import_path():
    func = discord_sync.get_import_path

    assert not hasattr(func, '__wrapped__')
    assert discord_sync.get_import_path(func) == 'juniorguru.lib.discord_sync.get_import_path'


def test_get_import_path_with_decorator():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    func = decorator(discord_sync.get_import_path)

    assert hasattr(func, '__wrapped__')
    assert discord_sync.get_import_path(func) == 'juniorguru.lib.discord_sync.get_import_path'


def test_get_import_path_with_db_connection_decorator():
    db = SqliteDatabase(':memory:')
    func = db.connection_context()(discord_sync.get_import_path)

    assert hasattr(func, '__wrapped__')
    assert discord_sync.get_import_path(func) == 'juniorguru.lib.discord_sync.get_import_path'
