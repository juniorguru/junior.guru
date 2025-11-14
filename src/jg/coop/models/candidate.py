import itertools
from enum import StrEnum, auto
from operator import attrgetter
from typing import Iterable, Self

from peewee import (
    BooleanField,
    CharField,
    Check,
    DateField,
    ForeignKeyField,
    IntegerField,
)
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

from jg.coop.lib.location import REGIONS, Location, repr_locations
from jg.coop.lib.text import get_tag_slug
from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubUser


class TagType(StrEnum):
    LOCATION = auto()
    SKILL = auto()
    LANGUAGE = auto()


class Tag(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)

    slug: str
    type: TagType

    @property
    def name(self) -> str:
        return f"#{self.slug}"


class Candidate(BaseModel):
    github_username = CharField(primary_key=True)
    github_url = CharField()
    user = ForeignKeyField(ClubUser, null=True, unique=True)
    name = CharField()
    bio = CharField(null=True)
    email = CharField(null=True)
    avatar_url = CharField()
    avatar_is_default = BooleanField()
    avatar_path = CharField(null=True)
    location_raw = CharField(null=True)
    location = JSONField(null=True)
    linkedin_url = CharField(null=True)
    skills = JSONField(default=list)
    domains = JSONField(default=list)
    experience = JSONField(default=list)
    secondary_school = CharField(null=True)
    university = CharField(null=True)
    languages = JSONField(default=list)
    is_ready = BooleanField()
    is_member = BooleanField()

    @property
    def contact_url(self) -> str:
        if self.email:
            return f"mailto:{self.email}"
        if self.linkedin_url:
            return self.linkedin_url
        return self.github_url

    @property
    def tags(self) -> list[Tag]:
        tags = []
        for skill in self.skills:
            tags.append(Tag(slug=get_tag_slug(skill), type=TagType.SKILL))
        if self.location:
            slug = get_tag_slug(self.location["region"])
            tags.append(Tag(slug=slug, type=TagType.LOCATION))
        for lang in self.languages:
            tags.append(Tag(slug=get_tag_slug(lang), type=TagType.LANGUAGE))
        return tags

    @property
    def location_text(self) -> str:
        locations = [Location(**self.location)] if self.location else []
        return repr_locations(locations)

    @property
    def school_text(self) -> str:
        prefixes = {
            "it": "IT ",
            "math": "matematická ",
            "non_it": "",
        }
        schools = []
        if self.secondary_school != "non_it" or not self.university:
            schools.append(prefixes[self.secondary_school] + "střední")
        if self.university:
            schools.append(prefixes[self.university] + "vysoká")
        return ", ".join(schools)

    @property
    def experience_text(self) -> str:
        experience = []
        if self.list_projects.count() > 0:
            experience.append("vlastní projekty")
        for exp in self.experience:
            experience.append(
                {
                    "volunteering": "dobrovolnictví v IT",
                    "intern": "stáž v IT",
                    "trainee": "trainee v IT",
                    "employee": "práce v IT",
                }[exp]
            )
        return ", ".join(experience)

    @property
    def is_highlighted(self) -> bool:
        return self.is_ready and self.is_member

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(
            cls.is_ready.desc(), cls.is_member.desc(), cls.name
        )

    @classmethod
    def region_tags(cls) -> list[Tag]:
        return [
            Tag(slug=get_tag_slug(region), type=TagType.LOCATION) for region in REGIONS
        ]

    @classmethod
    def tags_by_type(cls) -> dict[str, list[Tag]]:
        tags = sorted(
            set(
                itertools.chain.from_iterable(
                    candidate.tags for candidate in cls.listing()
                )
            ),
            key=attrgetter("type", "slug"),
        )
        return {
            str(type).lower(): list(tags)
            for type, tags in itertools.groupby(tags, key=attrgetter("type"))
        }


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
