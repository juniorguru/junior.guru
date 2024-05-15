from typing import Iterable, Self

from peewee import CharField, ForeignKeyField

from jg.coop.models.base import BaseModel
from jg.coop.models.club import ClubUser


class Candidate(BaseModel):
    github_username = CharField()
    user = ForeignKeyField(ClubUser, null=True, unique=True)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select()

    @classmethod
    def from_api(cls, profile: dict) -> Self:
        return cls(
            github_username=profile["username"],
            user=profile.get("discord_id"),
        )
