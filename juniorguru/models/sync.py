from peewee import CharField, DateTimeField, FloatField

from juniorguru.models.base import BaseModel


class SyncCommand(BaseModel):
    name = CharField()
    started_at = DateTimeField()
    timing_sec = FloatField()
