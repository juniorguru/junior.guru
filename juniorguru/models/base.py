import time
import json
from pathlib import Path
from collections.abc import Set

import scrapy
from peewee import Model, SqliteDatabase, OperationalError
from playhouse.sqlite_ext import JSONField as BaseJSONField

from juniorguru.lib.log import get_log


log = get_log('db')


db_file = Path(__file__).parent / '..' / 'data' / 'data.db'
db = SqliteDatabase(db_file, check_same_thread=False)


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


def retry_when_db_locked(db, op, stats=None, retries=10, wait_sec=0.5):
    last_error = None
    for i in range(retries):
        try:
            with db:
                return op()
        except OperationalError as error:
            if str(error) == 'database is locked':
                log.debug(f"Database operation '{op.__qualname__}' failed! ({error}, attempt: {i + 1})")
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
