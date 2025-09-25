from collections import Counter
from typing import Iterable, Self

from peewee import CharField, IntegerField, TextField

from jg.coop.models.base import BaseModel
from jg.coop.models.club import ClubUser


class InterestRole(BaseModel):
    club_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    interest_name = CharField(unique=True)

    @classmethod
    def count(self) -> int:
        return self.select().count()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.interest_name)

    @classmethod
    def interests(cls, min_count: int = 10) -> list[tuple[str, int]]:
        counter = Counter()
        for member in ClubUser.members_listing():
            counter.update(member.initial_roles)
        roles_by_id = {role.club_id: role.interest_name for role in cls.select()}
        return [
            (roles_by_id[role_id], count)
            for role_id, count in counter.most_common()
            if role_id in roles_by_id and count >= min_count
        ]


class DocumentedRole(BaseModel):
    club_id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    mention = CharField(unique=True)
    slug = CharField(unique=True)
    description = TextField()
    position = IntegerField(unique=True)
    emoji = CharField(null=True)
    color = IntegerField(null=True)
    icon_path = CharField(null=True)

    @classmethod
    def get_by_slug(cls, slug) -> Self:
        if not slug:
            raise ValueError(repr(slug))
        return cls.select().where(cls.slug == slug).get()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.position)
