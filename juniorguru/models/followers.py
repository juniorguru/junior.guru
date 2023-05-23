from collections import defaultdict
from datetime import date
from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class Followers(BaseModel):
    month = CharField(index=True)
    name = CharField()
    count = IntegerField()

    @classmethod
    def breakdown(cls, date: date) -> dict[str, int]:
        breakdown = defaultdict(int)
        for followers in cls.select().where(cls.month == f'{date:%Y-%m}'):
            breakdown[followers.name] += followers.count
        return dict(breakdown)
