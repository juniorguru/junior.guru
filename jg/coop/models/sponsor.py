from typing import Iterable, Self

from peewee import BooleanField, CharField, DateField, ForeignKeyField, TextField, fn

from jg.coop.models.base import BaseModel


class SponsorTier(BaseModel):
    slug = CharField(primary_key=True)


class Sponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()
    tier = ForeignKeyField(SponsorTier, backref="list_sponsors", null=True)
    renews_on = DateField()
    note = TextField(null=True)

    @classmethod
    def count(cls) -> int:
        return cls.select().count()


class PastSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()

    @classmethod
    def count(cls) -> int:
        return cls.select().count()


class GitHubSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField(null=True)
    url = CharField()
    avatar_path = CharField()
    is_active = BooleanField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .where(cls.is_active == True)  # noqa: E712
            .order_by(fn.random())
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()
