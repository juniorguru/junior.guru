import time
import json
from pathlib import Path
from collections.abc import Set
import asyncio

import scrapy
from peewee import Model, SqliteDatabase as BaseSqliteDatabase, OperationalError, ConnectionContext as BaseConnectionContext
from playhouse.sqlite_ext import JSONField as BaseJSONField

from juniorguru.lib import loggers


DB_FILE = Path(__file__).parent / '..' / 'data' / 'data.db'


logger = loggers.get(__name__)


class ConnectionContext(BaseConnectionContext):
    """Supports async functions when used as decorator"""
    def __call__(self, fn):
        if asyncio.iscoroutinefunction(fn):
            async def wrapper(*args, **kwargs):
                with self:
                    return (await fn(*args, **kwargs))
            return wrapper
        return super().__call__(fn)


class SqliteDatabase(BaseSqliteDatabase):
    def connection_context(self):
        return ConnectionContext(self)


db = SqliteDatabase(DB_FILE, pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    class Meta:
        database = db


class JSONField(BaseJSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('json_dumps', json_dumps)
        super().__init__(*args, **kwargs)


def json_dumps(value):
    def default(o):
        if isinstance(o, scrapy.Item):
            return dict(o)
        if isinstance(o, Set):
            return list(o)
        try:
            return o.isoformat()
        except AttributeError:
            raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

    return json.dumps(value, ensure_ascii=False, default=default)


def retry_when_db_locked(db, op, stats=None, retries=10, wait_sec=0.1):
    last_error = None
    for i in range(retries):
        try:
            with db:
                return op()
        except OperationalError as error:
            if str(error) == 'database is locked':
                logger.debug(f"Database operation '{op.__qualname__}' failed! ({error}, attempt: {i + 1})")
                last_error = error
                if stats:
                    stats.inc_value('database/locked_retries')
                time.sleep(wait_sec * i)
            else:
                if stats:
                    stats.inc_value('database/uncaught_errors')
                raise
    if stats:
        stats.inc_value('database/uncaught_errors')
    raise last_error
