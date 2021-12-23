import math
import functools
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
        year_ago = get_year_ago(today)
        return cls.select() \
            .where(cls.happened_on >= year_ago, cls.happened_on <= today) \
            .order_by(cls.happened_on.desc())

    @classmethod
    def incomes(cls, today=None):
        return cls.listing(today) \
            .where(cls.amount >= 0, cls.category != 'tax')

    @classmethod
    def incomes_breakdown(cls, today=None):
        return sum_by_category(cls.incomes(today))

    @classmethod
    def revenue(cls, today=None):
        return sum(transaction.amount for transaction in cls.incomes(today))

    @classmethod
    def revenue_monthly(cls, today=None):
        return math.ceil(cls.revenue(today) / 12.0)

    @classmethod
    def recurring_revenue(cls, today=None):
        incomes = cls.incomes_breakdown(today)
        return incomes.get('donations', 0) + incomes.get('memberships', 0)

    @classmethod
    def recurring_revenue_monthly(cls, today=None):
        return math.ceil(cls.recurring_revenue(today) / 12.0)

    @classmethod
    def expenses(cls, today=None):
        return cls.listing(today) \
            .where(((cls.amount < 0) & (cls.category != 'salary')) |
                   (cls.category == 'tax'))

    @classmethod
    def expenses_breakdown(cls, today=None):
        return {category: abs(value) for category, value
                in sum_by_category(cls.expenses(today)).items()}

    @classmethod
    def cost(cls, today=None):
        return abs(sum(transaction.amount for transaction in cls.expenses(today)))

    @classmethod
    def cost_monthly(cls, today=None):
        return math.ceil(cls.cost(today) / 12.0)

    @classmethod
    def profit(cls, today=None):
        return cls.revenue(today) - cls.cost(today)

    @classmethod
    def profit_monthly(cls, today=None):
        return math.ceil(cls.profit(today) / 12.0)


def sum_by_category(transactions):
    def reduce_step(mapping, transaction):
        mapping.setdefault(transaction.category, 0)
        mapping[transaction.category] += transaction.amount
        return mapping
    return functools.reduce(reduce_step, transactions, {})


def get_year_ago(today):
    try:
        return today.replace(year=today.year - 1)
    except ValueError:  # 29th February
        return today.replace(year=today.year - 1, day=today.day - 1)
