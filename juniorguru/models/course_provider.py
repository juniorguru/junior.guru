from typing import Iterable
from peewee import CharField, fn

from juniorguru.models.base import BaseModel


class CourseProvider(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()

    @property
    def edit_url(self) -> str:
        return ('https://github.com/honzajavorek/junior.guru/'
                'blob/main/juniorguru/data/course_providers/{self.slug}.yml')

    @classmethod
    def listing(cls) -> Iterable['CourseProvider']:
        return cls.select().order_by(fn.lower(cls.name))

    @classmethod
    def get_by_slug(cls, slug) -> 'CourseProvider':
        return cls.get(cls.slug == slug)
