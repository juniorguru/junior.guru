from peewee import CharField, DateField

from jg.coop.models.base import BaseModel


class Wisdom(BaseModel):
    date = DateField(index=True)
    text = CharField()
    name = CharField()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.date.desc())
