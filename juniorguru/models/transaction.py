import functools
import math

from peewee import CharField, DateField, IntegerField

from juniorguru.lib.charts import month_range, ttm_range
from juniorguru.models.base import BaseModel


class Transaction(BaseModel):
    happened_on = DateField(index=True)
    category = CharField()
    amount = IntegerField()

    @classmethod
    def listing(cls, from_date, to_date):
        return cls.select() \
            .where(cls.happened_on >= from_date, cls.happened_on <= to_date) \
            .order_by(cls.happened_on.desc())

    @classmethod
    def incomes(cls, from_date, to_date):
        return cls.listing(from_date, to_date) \
            .where(cls.amount >= 0, cls.category.not_in(['tax', 'sideline']))

    @classmethod
    def revenue(cls, date):
        return sum(transaction.amount for transaction
                   in cls.incomes(*month_range(date)))

    @classmethod
    def revenue_ttm(cls, date):
        return math.ceil(sum(transaction.amount for transaction
                             in cls.incomes(*ttm_range(date))) / 12.0)

    @classmethod
    def revenue_breakdown(cls, date):
        return sum_by_category(cls.incomes(*month_range(date)))

    @classmethod
    def revenue_ttm_breakdown(cls, date):
        return {category: math.ceil(value / 12) for category, value
                in sum_by_category(cls.incomes(*ttm_range(date))).items()}

    @classmethod
    def expenses(cls, from_date, to_date):
        return cls.listing(from_date, to_date) \
            .where(((cls.amount < 0) & (cls.category != 'salary')) |
                   (cls.category == 'tax'))

    @classmethod
    def cost(cls, date):
        return -1 * sum(transaction.amount for transaction
                        in cls.expenses(*month_range(date)))

    @classmethod
    def cost_ttm(cls, date):
        return math.ceil((-1 * sum(transaction.amount for transaction
                                   in cls.expenses(*ttm_range(date)))) / 12.0)

    @classmethod
    def cost_breakdown(cls, date):
        return {category: -1 * value for category, value
                in sum_by_category(cls.expenses(*month_range(date))).items()}

    @classmethod
    def profit(cls, date):
        return cls.revenue(date) - cls.cost(date)

    @classmethod
    def profit_ttm(cls, date):
        return cls.revenue_ttm(date) - cls.cost_ttm(date)


def sum_by_category(transactions):
    def reduce_step(mapping, transaction):
        mapping.setdefault(transaction.category, 0)
        mapping[transaction.category] += transaction.amount
        return mapping
    return functools.reduce(reduce_step, transactions, {})
