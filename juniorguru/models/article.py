from peewee import DateTimeField, CharField, BooleanField

from .base import BaseModel


class Article(BaseModel):
    url = CharField()
    date = DateTimeField(index=True)
    title = CharField()
    description = CharField()
