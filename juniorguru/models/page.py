from peewee import CharField, TextField, IntegerField

from juniorguru.models.base import BaseModel, JSONField


class Page(BaseModel):
    src_uri = CharField(unique=True)
    dest_uri = CharField(unique=True)
    size = IntegerField()
    meta = JSONField(default=dict)
    notes = TextField(null=True)

    @property
    def notes_size(self):
        return len(self.notes) if self.notes else 0

    @classmethod
    def handbook_listing(cls):
        return cls.select() \
            .where(cls.src_uri.startswith('handbook/')) \
            .order_by(cls.src_uri)
