import asyncio
import hashlib
import json
import pickle
import sqlite3
from collections.abc import Set
from enum import Enum
from functools import cache, wraps
from pathlib import Path
from typing import Iterable

from czech_sort import bytes_key as czech_sort_key
from peewee import (
    Check,
    ConnectionContext as BaseConnectionContext,
    Model,
    Node,
    SqliteDatabase as BaseSqliteDatabase,
)
from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import JSONField as BaseJSONField

from jg.coop.lib import loggers


DB_FILE = Path("src/jg/coop/data/data.db")

SQLITE_INT_MIN = -(1 << 63)

SQLITE_INT_MAX = (1 << 63) - 1


logger = loggers.from_path(__file__)


sqlite3.enable_callback_tracebacks(True)


class ConnectionContext(BaseConnectionContext):
    """Supports async functions when used as decorator"""

    def __call__(self, fn):
        if asyncio.iscoroutinefunction(fn):

            @wraps(fn)
            async def wrapper(*args, **kwargs):
                with self:
                    return await fn(*args, **kwargs)

            return wrapper
        return super().__call__(fn)


class SqliteDatabase(BaseSqliteDatabase):
    def connection_context(self):
        return ConnectionContext(self)


db = SqliteDatabase(DB_FILE, pragmas={"journal_mode": "wal"})


db.func("czech_sort")(cache(czech_sort_key))


class BaseModel(Model):
    class Meta:
        database = db

    def clear_dirty_fields(self):
        self._dirty = set()


class JSONField(BaseJSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("json_dumps", json_dumps)
        super().__init__(*args, **kwargs)


def json_dumps(value):
    def default(o):
        if isinstance(o, Set):
            return list(o)
        try:
            return o.isoformat()
        except AttributeError:
            raise TypeError(
                f"Object of type {o.__class__.__name__} is not JSON serializable"
            )

    return json.dumps(value, ensure_ascii=False, default=default)


def hash_models(models: list[BaseModel], **model_to_dict_kwargs) -> str:
    dicts = [model_to_dict(model, **model_to_dict_kwargs) for model in models]
    return hashlib.sha256(pickle.dumps(dicts)).hexdigest()


def check_enum(field_name: str, enum_cls: Enum) -> Node:
    return check(field_name, (member.value for member in enum_cls))


def check(field_name: str, iterable: Iterable) -> Node:
    values = tuple(iterable)
    sql = f"{field_name} in {values!r}"
    return Check(sql)
