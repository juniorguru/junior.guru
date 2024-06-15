from typing import Iterable, Self

from peewee import (
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    TextField,
    fn,
)

from jg.coop.models.base import BaseModel


class SponsorTier(BaseModel):
    slug = CharField(primary_key=True)
    priority = IntegerField()

    @property
    def list_sponsors(cls) -> Iterable["Sponsor"]:
        return cls._list_sponsors.order_by(Sponsor.name)


class Sponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()
    tier = ForeignKeyField(SponsorTier, backref="_list_sponsors", null=True)
    renews_on = DateField()
    note = TextField(null=True)
    coupon = CharField(null=True, index=True)
    # logo_path = CharField()
    # poster_path = CharField()
    # role_id = IntegerField(null=True)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .join(SponsorTier)
            .order_by(SponsorTier.priority.desc(), Sponsor.name)
        )

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
