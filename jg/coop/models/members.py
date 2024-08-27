import itertools
import json
from datetime import date
from typing import Iterable, Self

from peewee import CharField, IntegerField
from playhouse.shortcuts import model_to_dict

from jg.coop.models.base import BaseModel, check
from jg.coop.models.club import SubscriptionType


SUBSCRIPTION_TYPES_PREFIX = "subscription_types_"

NAMES = [
    "members",
    "members_f",
    "subscriptions_quits",
    "subscriptions_signups",
    "subscriptions_trials",
] + [
    f"{SUBSCRIPTION_TYPES_PREFIX}{subscription_type.lower()}"
    for subscription_type in SubscriptionType
]


class Members(BaseModel):
    class Meta:
        indexes = ((("month", "name"), True),)

    month = CharField(index=True)
    name = CharField(constraints=[check("name", NAMES)])
    count = IntegerField()

    @classmethod
    def deserialize(cls, line: str) -> Self | None:
        return cls.record(**json.loads(line))

    def serialize(self) -> str:
        data = model_to_dict(self, exclude=[self.__class__.id])
        return json.dumps(data, ensure_ascii=False) + "\n"

    @classmethod
    def record(cls, **kwargs) -> None:
        insert = cls.insert(**kwargs).on_conflict(
            action="update",
            update={cls.count: kwargs["count"]},
            conflict_target=[cls.month, cls.name],
        )
        insert.execute()

    @classmethod
    def history(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.month, cls.name)

    @classmethod
    def per_month(cls, name: str, months: Iterable[date]) -> list[int]:
        counts = {
            row.month: row.count
            for row in cls.select().where(cls.name == name).order_by(cls.month)
        }
        return [counts.get(month.strftime("%Y-%m"), None) for month in months]

    @classmethod
    def monthly_members(cls, months: Iterable[date]) -> list[int]:
        return cls.per_month("members", months)

    @classmethod
    def monthly_members_individuals(cls, months: Iterable[date]) -> list[int]:
        return [
            monthly + yearly
            for (monthly, yearly) in zip(
                cls.per_month("subscription_types_monthly", months),
                cls.per_month("subscription_types_yearly", months),
            )
        ]

    @classmethod
    def monthly_members_women_ptc(cls, months: Iterable[date]) -> list[float]:
        return [
            (count_women * 100) / count_total
            for (count_total, count_women) in zip(
                cls.per_month("members", months),
                cls.per_month("members_f", months),
            )
        ]

    @classmethod
    def monthly_subscription_types_breakdown(
        cls, months: Iterable[date]
    ) -> dict[str, list[int]]:
        subscription_types = set(
            itertools.chain.from_iterable(
                cls.select(cls.name)
                .where(cls.name.startswith(SUBSCRIPTION_TYPES_PREFIX))
                .distinct()
                .tuples()
            )
        )
        print(subscription_types)
        return {
            name.removeprefix(SUBSCRIPTION_TYPES_PREFIX): cls.per_month(name, months)
            for name in subscription_types
        }
