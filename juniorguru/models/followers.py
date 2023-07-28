from datetime import date
import json
from typing import Iterable, Self

from peewee import CharField, IntegerField, Case
from playhouse.shortcuts import model_to_dict

from juniorguru.models.base import BaseModel


class Followers(BaseModel):
    class Meta:
        indexes = (
            (('month', 'name'), True),
        )

    month = CharField(index=True)
    name = CharField()
    count = IntegerField()

    @classmethod
    def deserialize(cls, line: str) -> Self | None:
        data = json.loads(line)
        data['month'] = data.pop('_month')
        if data['count'] is not None:
            return cls.add(**data)

    def serialize(self) -> str:
        data = model_to_dict(self)
        del data['id']  # irrelevant
        data['_month'] = data.pop('month')
        return json.dumps(data, sort_keys=True, ensure_ascii=False) + '\n'

    @classmethod
    def add(cls, **kwargs) -> None:
        unique_key_fields = cls._meta.indexes[0][0]
        conflict_target = [getattr(cls, field) for field in unique_key_fields]
        update = {cls.count: Case(None, [(cls.count < kwargs['count'], kwargs['count'])], cls.count)}
        insert = cls.insert(**kwargs) \
            .on_conflict(action='update',
                         update=update,
                         conflict_target=conflict_target)
        insert.execute()

    @classmethod
    def history(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.month, cls.name)

    @classmethod
    def breakdown(cls, date: date) -> dict[str, int]:
        breakdown = {name: 0 for name in cls.names()}
        for followers in cls.select().where(cls.month == f'{date:%Y-%m}'):
            breakdown[followers.name] = max(breakdown[followers.name], followers.count)
        return breakdown

    @classmethod
    def names(cls) -> list[str]:
        query = cls.select(cls.name) \
            .distinct() \
            .order_by(cls.name)
        return [t[0] for t in query.tuples()]

    @classmethod
    def months_range(cls) -> tuple[date, date]:
        query = cls.select(cls.month) \
            .distinct() \
            .order_by(cls.month)
        tuples = query.tuples()
        from_date = date.fromisoformat(tuples[0][0] + '-01')
        to_date = date.fromisoformat(tuples[-1][0] + '-01')
        return from_date, to_date
