from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class Proxy(BaseModel):
    address = CharField(primary_key=True)
    speed_sec = IntegerField()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.speed_sec)
