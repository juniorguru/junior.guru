from peewee import CharField

from juniorguru.models.base import BaseModel


class Proxy(BaseModel):
    url = CharField()

    @classmethod
    def listing(cls):
        return cls.select()
