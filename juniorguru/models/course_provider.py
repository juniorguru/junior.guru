from peewee import CharField

from juniorguru.models.base import BaseModel


class CourseProvider(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.name)

    @classmethod
    def get_by_slug(cls, slug):
        return cls.get(cls.slug == slug)
