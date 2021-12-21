from datetime import date

from peewee import CharField, DateField, IntegerField

from juniorguru.models.base import BaseModel


class Transaction(BaseModel):
    happened_on = DateField(index=True)
    category = CharField()
    amount = IntegerField()

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        try:
            year_ago = today.replace(year=today.year - 1)
        except ValueError:  # 29th February
            year_ago = today.replace(year=today.year - 1, day=today.day - 1)

        return cls.select() \
            .where(cls.happened_on >= year_ago, cls.happened_on <= today) \
            .order_by(cls.happened_on.desc())

    # @classmethod
    # def incomes_breakdown(cls):
    #     pass
