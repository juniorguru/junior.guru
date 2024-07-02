from datetime import date
from itertools import groupby
from typing import TYPE_CHECKING, Iterable, Self

from peewee import (
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    TextField,
    fn,
)

from jg.coop.lib.discord_club import ClubChannelID, ClubEmoji
from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubMessage, ClubUser


if TYPE_CHECKING:
    from jg.coop.models.course_provider import CourseProvider


class SponsorTier(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField()
    priority = IntegerField()
    icon = CharField(null=True)
    price = IntegerField(null=True)
    member_price = IntegerField(null=True)
    plans = JSONField(default=list)
    max_sponsors = IntegerField(null=True)

    @property
    def url(self) -> str:
        return f"https://junior.guru/love/#{self.anchor}"

    @property
    def plan_url(self) -> str:
        return f"https://juniorguru.memberful.com/checkout?plan={self.plans[0]}"

    @property
    def anchor(self) -> str:
        return f"tier-{self.slug.replace('_', '-')}"

    @property
    def list_sponsors(self) -> Iterable["Sponsor"]:
        return self._list_sponsors.order_by(Sponsor.name)

    @property
    def is_barter(self) -> bool:
        return self.priority == 0

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
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()
    cz_business_id = IntegerField(null=True)
    sk_business_id = IntegerField(null=True)
    tier = ForeignKeyField(SponsorTier, backref="_list_sponsors")
    start_on = DateField(null=True)
    renews_on = DateField()
    note = TextField(null=True)
    coupon = CharField(null=True, index=True)
    logo_path = CharField()
    poster_path = CharField()
    role_id = IntegerField(null=True)
    listed = BooleanField(default=True)

    @classmethod
    def get_for_course_provider(
        cls,
        slug: str,
        cz_business_id: int | None = None,
        sk_business_id: int | None = None,
    ) -> Self:
        if cz_business_id:
            query = cls.select().where(cls.cz_business_id == cz_business_id)
        elif sk_business_id:
            query = cls.select().where(cls.sk_business_id == sk_business_id)
        else:
            query = cls.select().where(
                cls.slug == slug,
                cls.cz_business_id.is_null(),
                cls.sk_business_id.is_null(),
            )
        sponsors = sorted(query, key=lambda sponsor: 0 if sponsor.slug == slug else 1)
        try:
            return sponsors[0]
        except IndexError:
            raise cls.DoesNotExist()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .join(SponsorTier)
            .where(cls.listed == True)  # noqa: E712
            .order_by(SponsorTier.priority.desc(), Sponsor.name)
        )

    @classmethod
    def handbook_listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .join(SponsorTier)
            .where(
                cls.listed == True,  # noqa: E712
                (
                    SponsorTier.priority
                    == SponsorTier.select(fn.max(SponsorTier.priority)).scalar()
                ),
            )
            .order_by(Sponsor.name)
        )

    @classmethod
    def club_listing(cls) -> Iterable[Self]:
        return sorted(
            cls.listing(),
            key=lambda sponsor: (sponsor.members_count, sponsor.name),
            reverse=True,
        )

    @classmethod
    def tier_grouping(cls) -> list[tuple[SponsorTier, list[Self]]]:
        return [
            (tier, list(sponsors))
            for tier, sponsors in groupby(cls.listing(), lambda sponsor: sponsor.tier)
        ]

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def coupons(cls) -> set[str]:
        return frozenset(
            (
                row[0]
                for row in cls.select(cls.coupon)
                .distinct()
                .where(cls.coupon.is_null(False))
                .tuples()
            )
        )

    @property
    def name_markdown_bold(self) -> str:
        return f"**{self.name}**"

    @property
    def intro(self) -> ClubMessage:
        return ClubMessage.last_bot_message(
            ClubChannelID.INTRO,
            starting_emoji=ClubEmoji.SPONSOR_INTRO,
            contains_text=self.name_markdown_bold,
        )

    @property
    def course_provider(self) -> "CourseProvider | None":
        return self._course_provider.first()

    @property
    def list_members(self) -> Iterable[ClubUser]:
        if not self.coupon:
            return []
        cls = self.__class__
        return (
            ClubUser.select()
            .join(cls, on=(ClubUser.coupon == cls.coupon))
            .where(
                (ClubUser.is_member == True)  # noqa: E712
                & (ClubUser.coupon == self.coupon)
            )
            .order_by(ClubUser.display_name)
        )

    @property
    def members_count(self) -> int:
        return len(self.list_members)

    def days_until_renew(self, today=None) -> int:
        today = today or date.today()
        return max(0, (self.renews_on - today).days)


class PastSponsor(BaseModel):
    slug = CharField(primary_key=True)
    name = CharField()
    url = CharField()

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
