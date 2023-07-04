from typing import Iterable

from peewee import CharField, IntegerField, TextField

from juniorguru.models.base import BaseModel, JSONField


class Page(BaseModel):
    src_uri = CharField(unique=True)
    dest_uri = CharField(unique=True)
    meta = JSONField(default=dict)
    size = IntegerField(null=True)
    notes = TextField(null=True)
    thumbnail_path = CharField(null=True)

    @property
    def notes_size(self) -> int:
        return len(self.notes) if self.notes else 0

    @classmethod
    def get_by_src_uri(cls, src_uri) -> 'Page':
        return cls.get(cls.src_uri == src_uri)

    @classmethod
    def listing(cls) -> Iterable['Page']:
        return cls.select()

    @classmethod
    def handbook_listing(cls) -> Iterable['Page']:
        return cls.select() \
            .where(cls.src_uri.startswith('handbook/')) \
            .order_by(cls.src_uri)

    @classmethod
    def handbook_size_total(cls) -> int:
        return sum([page.size for page in cls.handbook_listing()])


class LegacyThumbnail(BaseModel):  # can be deleted once Flask is gone
    url = CharField(index=True, unique=True)
    image_path = CharField()

    @classmethod
    def image_path_by_url(cls, url: str) -> str:
        return cls.get(cls.url == url).image_path
