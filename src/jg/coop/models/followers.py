import json
from datetime import date
from typing import Iterable, Self

from peewee import Case, CharField, IntegerField
from playhouse.shortcuts import model_to_dict

from jg.coop.models.base import BaseModel


class Followers(BaseModel):
    class Meta:
        indexes = ((("month", "name"), True),)

    month = CharField(index=True)
    name = CharField()
    count = IntegerField()

    @classmethod
    def deserialize(cls, line: str) -> Self | None:
        data = json.loads(line)
        if data["count"] is not None:
            return cls.add(**data)

    def serialize(self) -> str:
        data = model_to_dict(self, exclude=[self.__class__.id])
        return json.dumps(data, ensure_ascii=False) + "\n"

    @classmethod
    def add(cls, **kwargs) -> None:
        update = {
            cls.count: Case(
                None, [(cls.count < kwargs["count"], kwargs["count"])], cls.count
            )
        }
        insert = cls.insert(**kwargs).on_conflict(
            action="update", update=update, conflict_target=[cls.month, cls.name]
        )
        insert.execute()

    @classmethod
    def history(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.month, cls.name)

    @classmethod
    def get_latest(cls, name: str) -> Self | None:
        return (
            cls.select()
            .where(cls.name == name)
            .order_by(cls.month.desc())
            .limit(1)
            .get()
        )

    @classmethod
    def breakdown(cls, date: date) -> dict[str, int]:
        breakdown = {name: None for name in cls.names()}
        for followers in cls.select().where(cls.month == f"{date:%Y-%m}"):
            breakdown[followers.name] = followers.count
        return breakdown

    @classmethod
    def names(cls) -> list[str]:
        query = cls.select(cls.name).distinct().order_by(cls.name)
        return [t[0] for t in query.tuples()]

    @classmethod
    def months_range(cls) -> tuple[date, date]:
        query = cls.select(cls.month).distinct().order_by(cls.month)
        tuples = query.tuples()
        from_date = date.fromisoformat(tuples[0][0] + "-01")
        to_date = date.fromisoformat(tuples[-1][0] + "-01")
        return from_date, to_date
