from datetime import date
from typing import TYPE_CHECKING, Iterable

from peewee import CharField, DateField, ForeignKeyField, IntegerField, fn

from juniorguru.lib.discord_club import ClubChannelID, ClubEmoji
from juniorguru.models.base import BaseModel, JSONField
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.models.job import ListedJob


if TYPE_CHECKING:
    from juniorguru.models.course_provider import CourseProvider


class Partner(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()
    coupon = CharField(null=True, index=True)
    logo_path = CharField(null=True)
    poster_path = CharField(null=True)
    role_id = IntegerField(null=True)

    @property
    def course_provider(self) -> "CourseProvider | None":
        return self._course_provider.first()

    @property
    def name_markdown_bold(self) -> str:
        return f"**{self.name}**"

    @property
    def list_members(self) -> Iterable[ClubUser]:
        if not self.coupon:
            return []
        return (
            ClubUser.select()
            .join(self.__class__, on=(ClubUser.coupon == self.__class__.coupon))
            .where(
                (ClubUser.is_member == True)  # noqa: E712
                & (ClubUser.coupon == self.coupon)
            )
            .order_by(ClubUser.display_name)
        )

    @property
    def list_jobs(self) -> Iterable[ListedJob]:
        return (
            ListedJob.submitted_listing()
            .join(self.__class__, on=(ListedJob.company_name == self.__class__.name))
            .where(ListedJob.company_name == self.name)
            .order_by(ListedJob.title)
        )

    @property
    def list_partnerships_history(self) -> Iterable["Partnership"]:
        return self.list_partnerships.order_by(Partnership.starts_on.desc())

    def active_partnership(self, today: date = None) -> "Partnership | None":
        today = today or date.today()
        return (
            self.list_partnerships.where(
                Partnership.starts_on <= today,
                (Partnership.expires_on >= today) | Partnership.expires_on.is_null(),
            )
            .order_by(Partnership.starts_on.desc())
            .first()
        )

    def first_partnership(self) -> "Partnership | None":
        return self.list_partnerships.order_by(Partnership.starts_on).first()

    @property
    def intro(self) -> ClubMessage:
        return ClubMessage.last_bot_message(
            ClubChannelID.INTRO,
            starting_emoji=ClubEmoji.PARTNER_INTRO,
            contains_text=self.name_markdown_bold,
        )

    @classmethod
    def get_by_slug(cls, slug: str) -> "Partner":
        return cls.get(cls.slug == slug)

    @classmethod
    def first_by_slug(cls, slug: str) -> "Partner | None":
        return cls.get_or_none(cls.slug == slug)

    @classmethod
    def active_listing(cls, today: date = None) -> Iterable["Partner"]:
        return [
            partnership.partner
            for partnership in Partnership.active_listing(today=today)
        ]

    @classmethod
    def expired_listing(cls, today: date = None) -> Iterable["Partner"]:
        today = today or date.today()
        return (
            cls.select()
            .join(Partnership)
            .group_by(cls)
            .having(
                fn.max(Partnership.starts_on) == Partnership.starts_on,
                Partnership.starts_on < today,
                Partnership.expires_on < today,
            )
            .order_by(cls.name)
        )

    @classmethod
    def coupons(cls) -> set[str]:
        return {
            partner.coupon for partner in cls.select().where(cls.coupon.is_null(False))
        }

    def __str__(self) -> str:
        return self.name


class PartnershipPlan(BaseModel):
    slug = CharField(unique=True)
    name = CharField()
    price = IntegerField()
    limit = IntegerField(null=True)
    includes = ForeignKeyField("self", null=True, backref="list_where_included")
    hierarchy_rank = IntegerField(null=True)

    @property
    def hierarchy(self) -> Iterable["PartnershipPlan"]:
        hierarchy = []
        plan = self
        while True:
            hierarchy.append(plan)
            if plan.includes:
                plan = plan.includes
            else:
                break
        return reversed(hierarchy)

    def benefits(self, all: bool = True) -> Iterable["PartnershipBenefit"]:
        for plan in self.hierarchy if all else [self]:
            yield from plan.list_benefits.order_by(PartnershipBenefit.position)

    def benefits_slugs(self, **kwargs) -> list[str]:
        return [benefit.slug for benefit in self.benefits(**kwargs)]

    @classmethod
    def get_by_slug(cls, slug) -> "PartnershipPlan":
        return cls.select().where(cls.slug == slug).get()


class PartnershipBenefit(BaseModel):
    position = IntegerField()
    text = CharField()
    icon = CharField()
    plan = ForeignKeyField(PartnershipPlan, backref="list_benefits")
    slug = CharField(unique=True)


class Partnership(BaseModel):
    partner = ForeignKeyField(Partner, backref="list_partnerships")
    plan = ForeignKeyField(PartnershipPlan, null=True, backref="list_partnerships")
    starts_on = DateField(index=True)
    expires_on = DateField(null=True, index=True)
    benefits_registry = JSONField(default=list)
    agreements_registry = JSONField(default=list)

    @property
    def page_url(self) -> str:
        return f"open/{self.partner.slug}.md"

    @classmethod
    def active_listing(
        cls, today: date = None, include_barters: bool = True
    ) -> Iterable["Partnership"]:
        today = today or date.today()
        expires_after_today = cls.expires_on >= today
        if include_barters:
            expires_after_today = expires_after_today | cls.expires_on.is_null()
        return (
            cls.select()
            .join(Partner)
            .switch(cls)
            .join(PartnershipPlan)
            .where(cls.starts_on <= today, expires_after_today)
            .order_by(PartnershipPlan.hierarchy_rank.desc(), Partner.name)
        )

    @classmethod
    def handbook_listing(cls, today: date = None) -> Iterable["Partnership"]:
        today = today or date.today()
        return (
            cls.active_listing(today=today)
            .switch(PartnershipPlan)
            .join(PartnershipBenefit)
            .where(PartnershipBenefit.slug == "logo_handbook")
        )

    def days_until_expires(self, today=None) -> int | None:
        today = today or date.today()
        if self.expires_on:
            return max(0, (self.expires_on - today).days)
        else:
            return None

    def evaluate_benefits(self, evaluators=None) -> list[dict[str, str | bool]]:
        registry = {
            benefit["slug"]: benefit.get("done", False)
            for benefit in self.benefits_registry
        }
        if evaluators:
            registry = {slug: fn_(self) for slug, fn_ in evaluators.items()} | registry
        return [
            dict(
                slug=benefit.slug,
                icon=benefit.icon,
                text=benefit.text,
                done=registry.get(benefit.slug, False),
            )
            for benefit in self.plan.benefits()
        ]
