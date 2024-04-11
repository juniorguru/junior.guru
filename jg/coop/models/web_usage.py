from datetime import date

from peewee import CharField, DateField, IntegerField

from jg.coop.models.base import BaseModel


class WebUsage(BaseModel):
    product_slug = CharField()
    month_starts_on = DateField(index=True)
    pageviews = IntegerField()

    @classmethod
    def months_range(cls) -> tuple[date, date]:
        query = cls.select(cls.month_starts_on).distinct().order_by(cls.month_starts_on)
        tuples = query.tuples()
        return tuples[0][0], tuples[-1][0]

    @classmethod
    def products(cls) -> list[str]:
        query = cls.select(cls.product_slug).distinct().order_by(cls.product_slug)
        return [t[0] for t in query.tuples()]

    @classmethod
    def breakdown(cls, date: date) -> dict[str, int]:
        breakdown = {product_slug: 0 for product_slug in cls.products()}
        for usage in cls.select().where(cls.month_starts_on == date.replace(day=1)):
            breakdown[usage.product_slug] = max(
                breakdown[usage.product_slug], usage.pageviews
            )
        return breakdown
