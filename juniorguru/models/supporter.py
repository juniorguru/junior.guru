import czech_sort
from peewee import CharField

from juniorguru.models.base import BaseModel


def sort_key(supporter):
    return czech_sort.key(supporter.last_name)


class Supporter(BaseModel):
    name = CharField()
    last_name = CharField()
    url = CharField(null=True)

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def listing_names_urls(cls):
        return sorted(cls.select().where(cls.url.is_null(False)), key=sort_key)

    @classmethod
    def listing_names(cls):
        return sorted(cls.select().where(cls.url.is_null()), key=sort_key)
