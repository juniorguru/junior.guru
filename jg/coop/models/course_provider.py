import itertools
from enum import StrEnum
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Self

import czech_sort
from peewee import CharField, IntegerField, TextField, fn

from jg.coop.models.base import BaseModel
from jg.coop.models.partner import Partner
from jg.coop.models.sponsor import Sponsor, SponsorTier


class CourseProviderGroup(StrEnum):
    HIGHLIGHTED = "highlighted"
    PARTNERS = "partners"
    OTHERS = "others"


class CourseUP(BaseModel):
    id = IntegerField(primary_key=True)
    url = CharField()
    name = CharField()
    description = TextField()
    company_name = CharField()
    business_id = IntegerField(index=True)

    @classmethod
    def add(cls, **kwargs) -> None:
        cls.insert(**kwargs).on_conflict_ignore().execute()

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def course_provider_listing(cls, business_id: int) -> Iterable[Self]:
        return (
            cls.select()
            .where(cls.business_id == business_id)
            .order_by(fn.czech_sort(cls.name))
        )


class CourseProvider(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()
    cz_business_id = IntegerField(null=True, index=True)
    cz_name = CharField(null=True)
    cz_legal_form = CharField(null=True)
    cz_years_in_business = IntegerField(null=True)
    sk_business_id = IntegerField(null=True, index=True)
    sk_name = CharField(null=True)
    sk_legal_form = CharField(null=True)
    sk_years_in_business = IntegerField(null=True)
    edit_url = CharField()
    page_title = CharField()
    page_description = CharField()
    page_lead = CharField()
    page_monthly_pageviews = IntegerField(null=True)
    usp_description = TextField(null=True)  # unique selling proposition

    @property
    def page_url(self) -> str:
        return f"courses/{self.slug}.md"

    @property
    def group(self) -> CourseProviderGroup:
        if org := self.organization:
            if isinstance(org, Sponsor) and org.tier.courses_highlight:
                return CourseProviderGroup.HIGHLIGHTED
            if isinstance(org, Partner):
                return CourseProviderGroup.PARTNERS
        return CourseProviderGroup.OTHERS

    @property
    def list_courses_up(self) -> Iterable[CourseUP]:
        return CourseUP.course_provider_listing(self.cz_business_id)

    @property
    def organization(self) -> Sponsor | Partner | None:
        orgs = list(itertools.chain(Sponsor.listing(), Partner.listing()))
        if self.cz_business_id:
            orgs = (org for org in orgs if org.cz_business_id == self.cz_business_id)
        elif self.sk_business_id:
            orgs = (org for org in orgs if org.sk_business_id == self.sk_business_id)
        else:
            orgs = (
                org
                for org in orgs
                if (
                    org.cz_business_id is None
                    and org.sk_business_id is None
                    and org.slug == self.slug
                )
            )
        orgs = sorted(orgs, key=lambda subject: 0 if subject.slug == self.slug else 1)
        try:
            return orgs[0]
        except IndexError:
            return None

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(fn.czech_sort(cls.name))

    @classmethod
    def grouping(cls) -> list[tuple[SponsorTier | None, list[Self]]]:
        groups = list(CourseProviderGroup)
        course_providers = sorted(
            cls.select(),
            key=lambda course_provider: (
                groups.index(course_provider.group),
                czech_sort.key(course_provider.name),
            ),
        )
        return [
            (group, list(sponsors))
            for group, sponsors in groupby(course_providers, attrgetter("group"))
        ]

    @classmethod
    def get_by_slug(cls, slug: str) -> Self:
        return cls.get(cls.slug == slug)

    def __str__(self) -> str:
        return self.name
