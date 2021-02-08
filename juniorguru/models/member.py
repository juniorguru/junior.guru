from peewee import CharField

from juniorguru.models.base import BaseModel


class Member(BaseModel):
    id = CharField(primary_key=True)
    avatar_url = CharField(null=True)

    @classmethod
    def count(cls):
        return cls.select().count()

    @classmethod
    def avatars_listing(cls):
        return cls.select().where(cls.avatar_url.is_null(False))
