from datetime import date
from functools import cached_property
from typing import Iterable

from peewee import CharField, ForeignKeyField, IntegerField, TextField, fn

from jg.coop.models.base import BaseModel
from jg.coop.models.partner import Partner, Partnership


class CourseProvider(BaseModel):
    name = CharField()
    slug = CharField(unique=True)
    url = CharField()
    cz_business_id = IntegerField(null=True)
    edit_url = CharField()
    page_title = CharField()
    page_description = CharField()
    page_lead = CharField()
    page_pageviews = IntegerField(null=True)
    partner = ForeignKeyField(
        Partner, backref="_course_provider", null=True, unique=True
    )

    # nemít description, ale schválně USP, aby bylo jasné, co je účelem popisku
    # https://en.wikipedia.org/wiki/Unique_selling_proposition

    @property
    def page_url(self) -> str:
        return f"courses/{self.slug}.md"

    def active_partnership(self, today: date = None) -> Partnership | None:
        return self.partner.active_partnership(today=today) if self.partner else None

    @cached_property
    def list_courses_up(self) -> Iterable["CourseUP"]:
        return (
            CourseUP.select()
            .where(CourseUP.cz_business_id == self.cz_business_id)
            .order_by(fn.czech_sort(CourseUP.name))
        )

    @classmethod
    def listing(cls, today: date = None) -> Iterable["CourseProvider"]:
        priority = [
            partner.course_provider
            for partner in Partner.active_listing(today=today)
            if partner.course_provider
        ]
        priority_slugs = [course_provider.slug for course_provider in priority]
        query = (
            cls.select()
            .where(cls.slug.not_in(priority_slugs))
            .order_by(fn.czech_sort(cls.name))
        )
        return priority + list(query)

    @classmethod
    def get_by_slug(cls, slug) -> "CourseProvider":
        return cls.get(cls.slug == slug)

    def __str__(self) -> str:
        return self.name


class CourseUP(BaseModel):
    id = IntegerField(primary_key=True)
    url = CharField()
    name = CharField()
    description = TextField()
    cz_business_id = IntegerField()

    @classmethod
    def count(cls) -> int:
        return cls.select().count()
