import json
from pathlib import Path

import scrapy
from peewee import Model, SqliteDatabase
from playhouse.sqlite_ext import JSONField as BaseJSONField


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
        try:
            return o.isoformat()
        except AttributeError:
            raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

    return json.dumps(value, ensure_ascii=False, default=default)
