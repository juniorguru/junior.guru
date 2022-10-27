from peewee import CharField, DateTimeField, FloatField

from juniorguru.models.base import BaseModel


class SyncCommand(BaseModel):
    name = CharField()
    started_at = DateTimeField()
    timing_sec = FloatField()
    sync_id = CharField(index=True)

    @classmethod
    def start(cls, sync_id=None):
        cls.drop_table()
        cls.create_table()

    @classmethod
    def record(cls):
        pass
