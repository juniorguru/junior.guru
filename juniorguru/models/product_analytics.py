from datetime import date

from peewee import CharField, DateField, IntegerField

from juniorguru.models.base import BaseModel


class ProductAnalytics(BaseModel):
    slug = CharField()
    starts_on = DateField(index=True)
    pageviews = IntegerField()

    @classmethod
    def months_range(cls) -> tuple[date, date]:
        query = cls.select(cls.starts_on) \
            .distinct() \
            .order_by(cls.starts_on)
        tuples = query.tuples()
        return tuples[0][0], tuples[-1][0]

    @classmethod
    def slugs(cls) -> list[str]:
        query = cls.select(cls.slug) \
            .distinct() \
            .order_by(cls.slug)
        return [t[0] for t in query.tuples()]

    @classmethod
    def breakdown(cls, date: date) -> dict[str, int]:
        breakdown = {slug: 0 for slug in cls.slugs()}
        for analytics in cls.select().where(cls.starts_on == date.replace(day=1)):
            breakdown[analytics.slug] = max(breakdown[analytics.slug], analytics.pageviews)
        return breakdown
