from typing import Iterable, Self

from peewee import CharField, DateTimeField

from jg.coop.models.base import BaseModel


class Meetup(BaseModel):
    title = CharField()
    starts_at = DateTimeField()
    ends_at = DateTimeField()
    location = CharField()
    region = CharField()
    url = CharField()
    series_name = CharField()
    series_org = CharField()
    series_url = CharField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.starts_at)
