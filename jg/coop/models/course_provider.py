from functools import cached_property
from typing import Iterable, Self

from peewee import CharField, ForeignKeyField, IntegerField, TextField, fn

from jg.coop.models.base import BaseModel
from jg.coop.models.sponsor import Sponsor, SponsorTier


class CourseProvider(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()
    cz_business_id = IntegerField(null=True)
    edit_url = CharField()
    page_title = CharField()
    page_description = CharField()
    page_lead = CharField()
    page_monthly_pageviews = IntegerField(null=True)
    sponsor = ForeignKeyField(
        Sponsor, backref="_course_provider", null=True, unique=True
    )
    usp_description = TextField(null=True)  # unique selling proposition

    @property
    def page_url(self) -> str:
        return f"courses/{self.slug}.md"

    @cached_property
    def list_courses_up(self) -> Iterable["CourseUP"]:
        return (
            CourseUP.select()
            .where(CourseUP.cz_business_id == self.cz_business_id)
            .order_by(fn.czech_sort(CourseUP.name))
        )

    @classmethod
    def sponsors_listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .join(Sponsor)
            .where(cls.sponsor.is_null(False))
            .join(SponsorTier)
            .order_by(SponsorTier.priority.desc(), fn.czech_sort(cls.name))
        )

    @classmethod
    def listing(cls) -> Iterable[Self]:
        priority = list(cls.sponsors_listing())
        priority_slugs = [course_provider.slug for course_provider in priority]
        query = (
            cls.select()
            .where(cls.slug.not_in(priority_slugs))
            .order_by(fn.czech_sort(cls.name))
        )
        return priority + list(query)

    @classmethod
    def get_by_slug(cls, slug: str) -> Self:
        return cls.get(cls.slug == slug)

    def __str__(self) -> str:
        return self.name


class CourseUP(BaseModel):
    id = IntegerField(primary_key=True)
    url = CharField()
    name = CharField()
    description = TextField()
    company_name = CharField()
    cz_business_id = IntegerField()

    @classmethod
    def count(cls) -> int:
        return cls.select().count()
