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
        try:
            year_ago = today.replace(year=today.year - 1)
        except ValueError:  # 29th February
            year_ago = today.replace(year=today.year - 1, day=today.day - 1)

        return cls.select() \
            .where(cls.happened_on >= year_ago, cls.happened_on <= today) \
            .order_by(cls.happened_on.desc())

    @classmethod
    def incomes_breakdown(cls, today=None):  # dodelat podle vzorce v excelu
        transactions = cls.listing(today) \
            .where(cls.amount >= 0, cls.category != 'tax')
        return sum_by_category(transactions)


    @classmethod
    def expenses_breakdown(cls, today=None):
        transactions = cls.listing(today) \
            .where(((cls.amount < 0) & (cls.category != 'salary')) |
                   (cls.category == 'tax'))
        return {category: abs(value) for category, value in sum_by_category(transactions).items()}


def sum_by_category(transactions):
    def reduce_step(mapping, transaction):
        mapping.setdefault(transaction.category, 0)
        mapping[transaction.category] += transaction.amount
        return mapping
    return functools.reduce(reduce_step, transactions, {})


def calc_ptc(breakdown_mapping):
    items = list(breakdown_mapping.items())
    total = sum(item[1] for item in items)
    return [(item[0], item[1], math.ceil(item[1] * 100 / total))
            for item in items]
