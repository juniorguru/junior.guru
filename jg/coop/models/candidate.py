from typing import Iterable, Self

from peewee import (
    BooleanField,
    CharField,
    Check,
    DateField,
    ForeignKeyField,
    IntegerField,
)

from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubUser


class Candidate(BaseModel):
    github_username = CharField(primary_key=True)
    github_url = CharField()
    user = ForeignKeyField(ClubUser, null=True, unique=True)
    name = CharField()
    bio = CharField(null=True)
    email = CharField(null=True)
    avatar_url = CharField()
    location = CharField(null=True)
    linkedin_url = CharField(null=True)
    topics = JSONField(default=list)
    domains = JSONField(default=list)
    experience = JSONField(default=list)
    secondary_school = CharField(null=True)
    university = CharField(null=True)
    languages = JSONField(default=list)
    is_ready = BooleanField()
    is_member = BooleanField()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(
            cls.is_ready.desc(), cls.is_member.desc(), cls.name
        )


class CandidateProject(BaseModel):
    name = CharField()
    candidate = ForeignKeyField(Candidate, backref="list_projects")
    title = CharField(null=True)
    source_url = CharField()
    live_url = CharField(null=True)
    description = CharField(null=True)
    priority = IntegerField(constraints=[Check("priority == 0 or priority == 1")])
    start_on = DateField()
    end_on = DateField()
    topics = JSONField(default=list)
