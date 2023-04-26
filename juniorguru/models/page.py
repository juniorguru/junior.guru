from peewee import CharField

from juniorguru.models.base import BaseModel, JSONField


class Page(BaseModel):
    src_uri = CharField(unique=True)
    dest_uri = CharField(unique=True)
    meta = JSONField(default=dict)
