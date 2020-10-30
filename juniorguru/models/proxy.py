from peewee import CharField

from juniorguru.models.base import BaseModel


class Proxy(BaseModel):
    address = CharField(primary_key=True)
