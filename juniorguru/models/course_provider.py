from typing import Iterable

from peewee import CharField, fn

from juniorguru.models.base import BaseModel


class CourseProvider(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()
    edit_url = CharField()
    page_title = CharField()
    page_description = CharField()
    page_lead = CharField()

    @classmethod
    def listing(cls) -> Iterable['CourseProvider']:
        return cls.select().order_by(fn.lower(cls.name))

    @classmethod
    def get_by_slug(cls, slug) -> 'CourseProvider':
        return cls.get(cls.slug == slug)

    def __str__(self) -> str:
        return self.name
