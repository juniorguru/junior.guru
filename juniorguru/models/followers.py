from datetime import date

from peewee import CharField, IntegerField

from juniorguru.models.base import BaseModel


class Followers(BaseModel):
    month = CharField(index=True)
    name = CharField()
    count = IntegerField()

    @classmethod
    def breakdown(cls, date: date) -> dict[str, int]:
        breakdown = {name: 0 for name in cls.names()}
        for followers in cls.select().where(cls.month == f'{date:%Y-%m}'):
            breakdown[followers.name] = max(breakdown[followers.name], followers.count)
        return breakdown

    @classmethod
    def names(cls) -> list[str]:
        query = cls.select(cls.name) \
            .distinct() \
            .order_by(cls.name)
        return [t[0] for t in query.tuples()]

    @classmethod
    def months_range(cls) -> tuple[date, date]:
        query = cls.select(cls.month) \
            .distinct() \
            .order_by(cls.month)
        tuples = query.tuples()
        from_date = date.fromisoformat(tuples[0][0] + '-01')
        to_date = date.fromisoformat(tuples[-1][0] + '-01')
        return from_date, to_date
