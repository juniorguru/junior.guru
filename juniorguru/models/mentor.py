from peewee import CharField, BooleanField, IntegerField, ForeignKeyField, fn

from juniorguru.models.base import BaseModel
from juniorguru.models.club import ClubUser


class Mentor(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    company = CharField(null=True)
    topics = CharField()
    book_url = CharField(null=True)
    message_url = CharField(unique=True, null=True)
    english_only = BooleanField(default=False)
    user = ForeignKeyField(ClubUser, unique=True)

    @classmethod
    def listing(cls):
        return cls.select(cls, ClubUser) \
            .join(ClubUser) \
            .order_by(fn.lower(ClubUser.display_name))

    @classmethod
    def interviews_listing(cls):
        return cls.listing() \
            .where(cls.topics.contains('pohovor'))
