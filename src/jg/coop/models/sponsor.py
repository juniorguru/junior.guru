from collections.abc import Iterable
from datetime import date
from typing import Literal, Self

import czech_sort
from peewee import BooleanField, CharField, DateField, IntegerField, TextField, fn

from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubUser


HANDBOOK_MAX_SPONSORS = 4


class Sponsor(BaseModel):
    # organization
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()
    cz_business_id = IntegerField(null=True)
    sk_business_id = IntegerField(null=True)
    subscription_id = IntegerField(null=True)
    logo_path = CharField()
    role_id = IntegerField(null=True)
    account_ids = JSONField(default=list)

    # sponsor
    start_on = DateField(null=True)
    renews_on = DateField()
    note = TextField(null=True)
    poster_path = CharField()

    @property
    def utm_campaign(self) -> Literal["sponsorship"]:
        return "sponsorship"

    @property
    def list_members(self) -> Iterable[ClubUser]:
        return ClubUser.select().where(ClubUser.account_id.in_(self.account_ids))

    @property
    def members_count(self) -> int:
        return len(self.account_ids)

    def to_guide_data(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "role_id": self.role_id,
            "members_count": self.members_count,
            "poster_path": self.poster_path,
        }

    def days_until_renew(self, today=None) -> int:
        today = today or date.today()
        return max(0, (self.renews_on - today).days)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(fn.czech_sort(cls.name))

    @classmethod
    def club_listing(cls) -> Iterable[Self]:
        return sorted(
            cls.listing(),
            key=lambda sponsor: (
                -1 * sponsor.members_count,
                czech_sort.key(sponsor.name),
            ),
        )

    @classmethod
    def handbook_listing(cls) -> list[Self]:
        sponsors = list(cls.listing())
        if len(sponsors) > HANDBOOK_MAX_SPONSORS:
            raise ValueError(
                f"Too many sponsors for the handbook logo bar: {len(sponsors)} "
                f"(max {HANDBOOK_MAX_SPONSORS})"
            )
        return sponsors

    @classmethod
    def count(cls) -> int:
        return cls.select().count()


class PastSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField(null=True)

    @property
    def utm_campaign(self) -> Literal["past-sponsorship"]:
        return "past-sponsorship"

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.name)


class GitHubSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField(null=True)
    url = CharField()
    avatar_path = CharField()
    is_active = BooleanField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().where(cls.is_active == True).order_by(cls.slug)

    @classmethod
    def past_listing(cls) -> Iterable[Self]:
        return cls.select().where(cls.is_active == False).order_by(cls.slug)

    @classmethod
    def count(cls) -> int:
        return cls.select().count()
