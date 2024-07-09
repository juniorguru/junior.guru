import json
from typing import Iterable, Self

from peewee import Case, CharField, IntegerField
from playhouse.shortcuts import model_to_dict

from jg.coop.models.base import BaseModel


class Members(BaseModel):
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
