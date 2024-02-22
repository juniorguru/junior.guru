from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class Stage(BaseModel):
    position = IntegerField(unique=True)
    slug = CharField(unique=True)
    title = CharField()
    icon = CharField(unique=True)
    description = CharField()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.position)
