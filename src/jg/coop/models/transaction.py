import functools
import json
import math
from datetime import date
from enum import StrEnum, unique
from typing import Iterable, Self

from peewee import CharField, DateField, IntegerField
from playhouse.shortcuts import model_to_dict

from jg.coop.lib.charts import month_range, ttm_range
from jg.coop.models.base import BaseModel, check_enum


@unique
class TransactionsCategory(StrEnum):
    MEMBERSHIPS = "memberships"
    DONATIONS = "donations"
    SPONSORSHIPS = "sponsorships"
    JOBS = "jobs"
    PRODUCTION = "production"
    LAWYER = "lawyer"
    MARKETING = "marketing"
    ACCOUNTING = "accounting"
    OFFICE = "office"
    FAKTUROID = "fakturoid"
    DISCORD = "discord"
    MEMBERFUL = "memberful"
    TAX = "tax"
    MISCELLANEOUS = "miscellaneous"
    IGNORE = "ignore"


class Transaction(BaseModel):
    id = CharField(primary_key=True)
    happened_on = DateField(index=True)
    category = CharField(constraints=[check_enum("category", TransactionsCategory)])
    amount = IntegerField()

    @classmethod
    def deserialize(cls, line: str):
        data = json.loads(line)
        data["id"] = data.pop("_id")
        data["happened_on"] = date.fromisoformat(data["happened_on"])
        return cls.create(**data)

    def serialize(self) -> str:
        data = model_to_dict(self)
        data["_id"] = data.pop("id")
        data["happened_on"] = data["happened_on"].isoformat()
        return json.dumps(data, sort_keys=True, ensure_ascii=False) + "\n"

    @classmethod
    def add(cls, **data) -> None:
        cls.replace(**data).execute()

    @classmethod
    def history_end_on(cls) -> date:
        return (
            cls.select(cls.happened_on)
            .order_by(cls.happened_on.desc())
            .limit(1)
            .scalar()
        )

    @classmethod
    def history(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.happened_on.asc())

    @classmethod
    def listing(cls, from_date, to_date):
        return (
            cls.select()
            .where(cls.happened_on >= from_date, cls.happened_on <= to_date)
            .order_by(cls.happened_on.desc())
        )

    @classmethod
    def incomes(cls, from_date, to_date):
        return cls.listing(from_date, to_date).where(
            cls.amount >= 0, cls.category != "tax"
        )

    @classmethod
    def revenue(cls, date):
        return sum(
            transaction.amount for transaction in cls.incomes(*month_range(date))
        )

    @classmethod
    def revenue_ttm(cls, date):
        return math.ceil(
            sum(transaction.amount for transaction in cls.incomes(*ttm_range(date)))
            / 12.0
        )

    @classmethod
    def revenue_breakdown(cls, date):
        return sum_by_category(cls.incomes(*month_range(date)))

    @classmethod
    def revenue_ttm_breakdown(cls, date):
        return {
            category: math.ceil(value / 12)
            for category, value in sum_by_category(
                cls.incomes(*ttm_range(date))
            ).items()
        }

    @classmethod
    def expenses(cls, from_date, to_date):
        return cls.listing(from_date, to_date).where(
            (cls.amount < 0) | (cls.category == "tax")
        )

    @classmethod
    def cost(cls, date):
        return -1 * sum(
            transaction.amount for transaction in cls.expenses(*month_range(date))
        )

    @classmethod
    def cost_ttm(cls, date):
        return math.ceil(
            (
                -1
                * sum(
                    transaction.amount for transaction in cls.expenses(*ttm_range(date))
                )
            )
            / 12.0
        )

    @classmethod
    def cost_breakdown(cls, date):
        return {
            category: -1 * value
            for category, value in sum_by_category(
                cls.expenses(*month_range(date))
            ).items()
        }

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
