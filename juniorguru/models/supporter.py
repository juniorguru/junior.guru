from peewee import CharField

from juniorguru.models.base import BaseModel


class Supporter(BaseModel):
    name = CharField()
    last_name = CharField()
    url = CharField(null=True)

    @classmethod
    def listing_names_urls(cls):
        return cls.select() \
            .where(cls.url.is_null(False)) \
            .order_by(cls.last_name)

    @classmethod
    def listing_names(cls):
        return cls.select() \
            .where(cls.url.is_null()) \
            .order_by(cls.last_name)
