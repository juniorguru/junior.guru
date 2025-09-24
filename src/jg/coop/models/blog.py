from typing import Iterable, Self

from peewee import CharField, DateField

from jg.coop.models.base import BaseModel


class BlogArticle(BaseModel):
    title = CharField()
    url = CharField()
    published_on = DateField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.published_on.desc())

    @classmethod
    def latest(cls) -> Self:
        return cls.listing().get()
