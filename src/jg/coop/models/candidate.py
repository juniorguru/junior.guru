import itertools
from datetime import timedelta
from enum import StrEnum, auto
from operator import attrgetter
from typing import Iterable, Self

from peewee import BooleanField, CharField, DateField, ForeignKeyField, IntegerField, fn
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.location import REGIONS, FuzzyLocation, Location, repr_locations
from jg.coop.lib.text import get_tag_slug
from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubChannel, ClubMessage, ClubUser


ANYWHERE_TAG_SLUG = "kdekoliv"


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


class Badge(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)

    icon: str
    label: str
    help_text: str


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
    location_fuzzy = JSONField(null=True)
    linkedin_url = CharField(null=True)
    skills = JSONField(default=list)
    domains = JSONField(default=list)
    experience = JSONField(default=list)
    secondary_school = CharField(null=True)
    university = CharField(null=True)
    languages = JSONField(default=list)
    is_ready = BooleanField()
    is_member = BooleanField()
    report_url = CharField(null=True)

    @property
    def tags(self) -> list[Tag]:
        tags = []
        for skill in self.skills:
            tags.append(Tag(slug=get_tag_slug(skill), type=TagType.SKILL))
        if not self.locations:
            tags.append(Tag(slug=ANYWHERE_TAG_SLUG, type=TagType.LOCATION))
        for location in self.locations:
            slug = get_tag_slug(location.region)
            tags.append(Tag(slug=slug, type=TagType.LOCATION))
        for lang in self.languages:
            tags.append(Tag(slug=get_tag_slug(lang), type=TagType.LANGUAGE))
        return tags

    @property
    def badges(self) -> list[Badge]:
        badges = []
        if projects_count := self.list_projects.count():
            match projects_count:
                case 1:
                    label = "1 projekt"
                case _ if projects_count in range(2, 5):
                    label = f"{projects_count} projekty"
                case _:
                    label = f"{projects_count} projektů"
            badges.append(
                Badge(
                    icon="tools",
                    label=label,
                    help_text="Počet připnutých projektů na GitHubu",
                )
            )

        knows_ai = (
            ClubMessage.select()
            .where(
                ClubMessage.author_id == self.user_id,
                ClubMessage.channel_id == ClubChannelID.AI,
            )
            .count()
            > 5
        )
        if knows_ai:
            badges.append(
                Badge(
                    icon="stars",
                    label="umí používat AI",
                    help_text="Na klubovém Discordu se aktivně účastní debat o umělé inteligenci",
                )
            )

        communicates_online = (
            ClubMessage.select().where(ClubMessage.author_id == self.user_id).count()
            > 50
        )
        if communicates_online:
            badges.append(
                Badge(
                    icon="chat",
                    label="dobře komunikuje na dálku",
                    help_text="Aktivně píše na klubovém Discordu",
                )
            )

        is_organized = (
            ClubMessage.select()
            .where(
                ClubMessage.author_id == self.user_id,
                ClubMessage.parent_channel_id == ClubChannelID.WEEKLY_PLANS,
            )
            .count()
            > 10
        )
        if is_organized:
            badges.append(
                Badge(
                    icon="calendar-check",
                    label="systematický přístup",
                    help_text="Pravidelně plánuje svůj týden na klubovém Discordu",
                )
            )

        has_feedback = (
            ClubChannel.select()
            .join(ClubMessage, on=(ClubChannel.id == ClubMessage.channel_id))
            .where(
                ClubChannel.author_id == self.user_id,
                ClubMessage.parent_channel_id.in_(
                    [ClubChannelID.CV_GITHUB_LINKEDIN, ClubChannelID.CREATIONS]
                ),
            )
            .count()
        )
        if has_feedback:
            badges.append(
                Badge(
                    icon="check2-square",
                    label="nebojí se zpětné vazby",
                    help_text="Žádá o zpětnou vazbu na klubovém Discordu (projekty, CV)",
                )
            )

        has_diary = (
            ClubChannel.select()
            .join(ClubMessage, on=(ClubChannel.id == ClubMessage.channel_id))
            .where(
                ClubChannel.author_id == self.user_id,
                ClubMessage.parent_channel_id == ClubChannelID.DIARIES,
            )
            .first()
        )
        if has_diary:
            badges.append(
                Badge(
                    icon="journals",
                    label="vede si deník",
                    help_text="Vede si deník o cestě do IT na klubovém Discordu",
                )
            )

        return badges

    @property
    def projects(self) -> Iterable["CandidateProject"]:
        return self.list_projects.order_by(CandidateProject.priority.desc())

    @property
    def locations(self) -> list[Location]:
        if self.location_fuzzy:
            location_fuzzy = FuzzyLocation(**self.location_fuzzy)
            if not location_fuzzy.is_universal and len(location_fuzzy.locations) < 3:
                return location_fuzzy.locations
        return []

    @property
    def location_text(self) -> str | None:
        return repr_locations(self.locations)

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
            cls.is_ready.desc(), cls.is_member.desc(), fn.random()
        )

    @classmethod
    def region_tags(cls) -> list[Tag]:
        return [Tag(slug=ANYWHERE_TAG_SLUG, type=TagType.LOCATION)] + [
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
    name = CharField(unique=True)
    candidate = ForeignKeyField(Candidate, backref="list_projects")
    title = CharField(null=True)
    source_url = CharField()
    demo_url = CharField(null=True)
    description = CharField(null=True)
    priority = IntegerField()
    start_on = DateField()
    end_on = DateField()
    topics = JSONField(default=list)

    @property
    def name_repo(self) -> str:
        return self.source_url.rstrip("/").split("/")[-1]

    @property
    def duration(self) -> timedelta:
        return self.end_on - self.start_on
