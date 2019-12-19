from peewee import DateTimeField, CharField, BooleanField

from .base import BaseModel


class Article(BaseModel):
    url = CharField()
    date = DateTimeField(index=True)
    title = CharField()
    description = CharField()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.date.desc())
