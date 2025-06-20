from datetime import date
from itertools import groupby
from typing import Iterable, Literal, Self

import czech_sort
from peewee import (
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    TextField,
    fn,
)

from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubUser


class SponsorTier(BaseModel):
    name = CharField()
    priority = IntegerField()
    price = IntegerField(null=True)
    member_price = IntegerField(null=True)
    plan_id = IntegerField()
    max_sponsors = IntegerField(null=True)
    courses_highlight = BooleanField(default=False)

    @property
    def url(self) -> str:
        return f"https://junior.guru/love/#{self.slug}"

    @property
    def plan_url(self) -> str:
        return f"https://juniorguru.memberful.com/checkout?plan={self.plans[0]}"

    @property
    def slug(self) -> str:
        return f"tier-{self.priority}"

    @property
    def list_sponsors(self) -> Iterable["Sponsor"]:
        return self._list_sponsors.order_by(Sponsor.name)

    @property
    def is_sold_out(self) -> bool:
        return (
            self.max_sponsors is not None
            and len(self.list_sponsors) >= self.max_sponsors
        )

    @classmethod
    def pricing_listing(cls) -> Iterable[Self]:
        return cls.select().where(cls.price.is_null(False)).order_by(cls.priority)


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
    tier = ForeignKeyField(SponsorTier, backref="_list_sponsors")
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

    def days_until_renew(self, today=None) -> int:
        today = today or date.today()
        return max(0, (self.renews_on - today).days)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .join(SponsorTier)
            .order_by(SponsorTier.priority.desc(), fn.czech_sort(cls.name))
        )

    @classmethod
    def club_listing(cls) -> Iterable[Self]:
        return sorted(
            cls.listing(),
            key=lambda sponsor: (
                -1 * sponsor.members_count,
                -1 * sponsor.tier.priority,
                czech_sort.key(sponsor.name),
            ),
        )

    @classmethod
    def tier_grouping(cls) -> list[tuple[SponsorTier, list[Self]]]:
        return [
            (tier, list(sponsors))
            for tier, sponsors in groupby(cls.listing(), lambda sponsor: sponsor.tier)
        ]

    @classmethod
    def handbook_listing(cls) -> Iterable[Self]:
        for _, sponsors in cls.tier_grouping():
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
        return (
            cls.select().where(cls.is_active == True).order_by(cls.slug)  # noqa: E712
        )

    @classmethod
    def past_listing(cls) -> Iterable[Self]:
        return (
            cls.select().where(cls.is_active == False).order_by(cls.slug)  # noqa: E712
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()
