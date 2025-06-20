import itertools
import json
import textwrap
from datetime import date, datetime, time, timedelta
from enum import StrEnum, auto
from operator import attrgetter
from typing import Iterable, Self
from urllib.parse import quote_plus

from peewee import (
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    IntegrityError,
    TextField,
    fn,
)
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

from jg.coop.lib.mapycz import REGIONS
from jg.coop.lib.text import get_tag_slug
from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubUser


JOB_EXPIRED_SOON_DAYS = 10

REMOTE_TAG_SLUG = "remote"


class TagType(StrEnum):
    EMPLOYMENT = auto()
    LOCATION = auto()
    TECHNOLOGY = auto()
    SOURCE = auto()


class Tag(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)

    slug: str
    type: TagType

    @property
    def name(self) -> str:
        return f"#{self.slug}"


class SubmittedJob(BaseModel):
    id = CharField(primary_key=True)
    boards_ids = JSONField(default=list, index=True)

    title = CharField()
    posted_on = DateField(index=True)
    expires_on = DateField(index=True)
    lang = CharField()
    description_html = TextField()
    description_text = TextField()

    url = CharField(unique=True)
    apply_email = CharField(null=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField()
    company_logo_urls = JSONField(default=list)

    locations_raw = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    def analytics_url(self, days, end_on=None):
        end_on = end_on or date.today()
        start_on = end_on - timedelta(days=days)
        return f"https://simpleanalytics.com/junior.guru?search=paths%3A{self.id}&start={start_on}&end={end_on}"

    def days_since_posted(self, today=None):
        today = today or date.today()
        return (today - self.posted_on).days

    def days_until_expires(self, today=None):
        today = today or date.today()
        return (self.expires_on - today).days

    def expires_soon(self, today=None):
        today = today or date.today()
        return self.days_until_expires(today=today) <= JOB_EXPIRED_SOON_DAYS

    @classmethod
    def date_listing(cls, date_):
        return cls.select().where((cls.posted_on <= date_) & (cls.expires_on >= date_))

    def to_listed(self):
        data = {
            field_name: getattr(self, field_name, None)
            for field_name in ListedJob._meta.fields.keys()
            if (
                field_name in self.__class__._meta.fields
                and field_name not in ["id", "submitted_job"]
            )
        }
        return ListedJob(submitted_job=self, reason=None, **data)


class ScrapedJob(BaseModel):
    boards_ids = JSONField(default=list, index=True)

    title = CharField()
    posted_on = DateField(index=True)
    lang = CharField(null=True)
    description_html = TextField()
    description_text = TextField()
    llm_opinion = JSONField(null=True)

    url = CharField(unique=True)
    apply_url = CharField(null=True)

    company_name = CharField()
    company_url = CharField(null=True)
    company_logo_urls = JSONField(default=list)

    locations_raw = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)

    source = CharField()
    source_urls = JSONField(default=list)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.posted_on.desc())

    @classmethod
    def get_by_item(cls, item) -> Self:
        return cls.select().where(cls.url == item["url"]).get()

    @classmethod
    def from_item(cls, item) -> Self:
        data = {
            field_name: item.get(field_name)
            for field_name in cls._meta.fields.keys()
            if field_name in item
        }
        data["posted_on"] = date.fromisoformat(item["posted_on"])
        return cls(**data)

    def to_item(self) -> dict:
        return model_to_dict(self)

    def merge_item(self, item):
        for field_name in self.__class__._meta.fields.keys():
            try:
                # use merging method if present
                merge_method = getattr(self, f"_merge_{field_name}")
                setattr(self, field_name, merge_method(item))
            except AttributeError:
                # overwrite with newer data
                posted_on = date.fromisoformat(item["posted_on"])
                if posted_on >= self.posted_on:
                    old_value = getattr(self, field_name)
                    new_value = item.get(field_name, old_value)
                    setattr(self, field_name, new_value)

    def _merge_boards_ids(self, item) -> list[str]:
        return list(set(self.boards_ids + item.get("boards_ids", [])))

    def _merge_items_hashes(self, item) -> list[str]:
        return list(set(self.items_hashes + item.get("items_hashes", [])))

    def _merge_source_urls(self, item) -> list[str]:
        return list(set(self.source_urls + item.get("source_urls", [])))

    def _merge_posted_on(self, item) -> date:
        posted_on = date.fromisoformat(item["posted_on"])
        return min(self.posted_on, posted_on)

    def _merge_items_merged_count(self, item) -> int:
        return self.items_merged_count + 1

    def to_listed(self) -> "ListedJob":
        data = {
            field_name: getattr(self, field_name, None)
            for field_name in ListedJob._meta.fields.keys()
            if (
                field_name in self.__class__._meta.fields
                and field_name not in ["id", "submitted_job"]
            )
        }
        return ListedJob(reason=self.llm_opinion["reason"], **data)


class DroppedJob(BaseModel):
    title = CharField()
    url = CharField()
    reason = CharField(null=True, index=True)

    @classmethod
    def from_item(cls, item) -> Self:
        return cls(
            title=item["title"],
            url=item["url"],
            reason=item["llm_opinion"]["reason"] if item.get("llm_opinion") else None,
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def sample_listing(cls, size: int) -> Iterable[Self]:
        return (
            cls.select()
            .where(cls.reason.is_null(False), cls.title ** "%junior%")
            .order_by(fn.random())
            .limit(size)
        )


class LogoSourceType(StrEnum):
    LOGO = "logo"
    ICON = "icon"


class ListedJob(BaseModel):
    boards_ids = JSONField(default=list, index=True)
    submitted_job = ForeignKeyField(SubmittedJob, unique=True, null=True)
    reason = CharField(null=True)

    title = CharField()
    posted_on = DateField(index=True)
    lang = CharField()
    description_html = TextField()
    description_text = TextField()

    url = CharField()
    apply_email = CharField(null=True)
    apply_url = CharField(null=True)

    discord_url = CharField(null=True)
    upvotes_count = IntegerField(null=True)
    comments_count = IntegerField(null=True)

    company_name = CharField()
    company_url = CharField(null=True)
    company_logo_urls = JSONField(default=list)
    company_logo_path = CharField(null=True)

    locations_raw = JSONField(null=True)
    locations = JSONField(null=True)
    remote = BooleanField(default=False)
    employment_types = JSONField(null=True)
    tech_tags = JSONField(default=list)

    @property
    def title_short(self) -> str:
        return textwrap.shorten(self.title, 90, placeholder="…")

    @property
    def initial(self) -> str | None:
        if self.company_name:
            return self.company_name[0].upper()
        return None

    @property
    def effective_url(self) -> str:
        if self.is_submitted:
            return self.url
        return self.apply_url or self.url

    @property
    def company_atmoskop_url(self) -> str:
        return f"https://www.atmoskop.cz/hledani?q={quote_plus(self.company_name)}"

    @property
    def company_search_url(self) -> str:
        return f"https://www.google.cz/search?q={quote_plus(self.company_name)}"

    @property
    def company_linkedin_url(self) -> str:
        return f"https://www.linkedin.com/search/results/companies/?keywords={quote_plus(self.company_name)}"

    @property
    def company_jakybylpohovor_url(self) -> str:
        utm_params = "&utm_source=junior.guru&utm_medium=web&utm_campaign=jobs"
        return f"https://www.jakybylpohovor.cz/search/?name={quote_plus(self.company_name)}{utm_params}"

    @property
    def is_submitted(self) -> bool:
        return bool(self.submitted_job)

    @property
    def is_highlighted(self) -> bool:
        return self.is_submitted

    @property
    def company_logo_source_urls(self) -> list[str]:
        return self.company_logo_urls + ([self.company_url] if self.company_url else [])

    def get_logo_source_type(self, logo_source_url: str) -> LogoSourceType | None:
        if logo_source_url in self.company_logo_urls:
            return LogoSourceType.LOGO
        if logo_source_url == self.company_url:
            return LogoSourceType.ICON
        return None

    @property
    def tags(self) -> list[Tag]:
        tags = []
        if self.remote:
            tags.append(Tag(slug=REMOTE_TAG_SLUG, type=TagType.LOCATION))
        for employment_type in self.employment_types or []:
            tags.append(Tag(slug=employment_type, type=TagType.EMPLOYMENT))
        for region in self.regions:
            tags.append(Tag(slug=get_tag_slug(region), type=TagType.LOCATION))
        for tech_tag in self.tech_tags:
            tags.append(Tag(slug=tech_tag, type=TagType.TECHNOLOGY))
        for source in self.sources:
            tags.append(Tag(slug=source, type=TagType.SOURCE))
        return tags

    @property
    def sources(self) -> list[str]:
        return [board_id.split("#")[0] for board_id in self.boards_ids]

    @property
    def regions(self) -> list[str]:
        return sorted(set(location["region"] for location in self.locations or []))

    @property
    def location(self) -> str:
        # TODO refactor, this is terrible
        locations = self.locations or []
        if len(locations) == 1:
            location = locations[0]
            place, region = location["place"], location["region"]
            parts = [place] if place == region else [place, region]
            if self.remote:
                parts.append("na dálku")
            parts = list(filter(None, parts))
            if parts:
                return ", ".join(parts)
            return "?"
        else:
            parts = list(sorted(filter(None, [loc["place"] for loc in locations])))
            if len(parts) > 2:
                parts = parts[:2]
                if self.remote:
                    parts[-1] += " a další"
                    parts.append("na dálku")
                    return ", ".join(parts)
                else:
                    return ", ".join(parts) + "…"
            elif parts:
                return ", ".join(parts + (["na dálku"] if self.remote else []))
            if self.remote:
                return "na dálku"
            return "?"

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def region_tags(cls) -> list[Tag]:
        return [Tag(slug=REMOTE_TAG_SLUG, type=TagType.LOCATION)] + [
            Tag(slug=get_tag_slug(region), type=TagType.LOCATION) for region in REGIONS
        ]

    @classmethod
    def tags_by_type(cls) -> dict[str, list[Tag]]:
        tags = sorted(
            set(itertools.chain.from_iterable(job.tags for job in cls.listing())),
            key=attrgetter("type", "slug"),
        )
        return {
            str(type).lower(): list(tags)
            for type, tags in itertools.groupby(tags, key=attrgetter("type"))
        }

    @classmethod
    def listing(cls) -> Iterable[Self]:
        upvotes_count = fn.coalesce(cls.upvotes_count, 0)
        comments_count = fn.coalesce(cls.comments_count, 0)
        return cls.select().order_by(
            cls.submitted_job.is_null(),
            (upvotes_count + comments_count).desc(),
            cls.posted_on.desc(),
        )

    @classmethod
    def no_logo_listing(cls) -> Iterable[Self]:
        return cls.select().where(cls.company_logo_path.is_null())

    @classmethod
    def no_discord_listing(cls) -> Iterable[Self]:
        return cls.select().where(cls.discord_url.is_null())

    @classmethod
    def submitted_listing(cls) -> Iterable[Self]:
        return cls.select().where(cls.submitted_job.is_null(False))

    @classmethod
    def get_by_submitted_id(cls, submitted_job_id) -> Iterable[Self]:
        return cls.select().where(cls.submitted_job == submitted_job_id).get()

    @classmethod
    def get_by_url(cls, url) -> Self:
        try:
            return cls.select().where(cls.url == url).get()
        except cls.DoesNotExist:
            return cls.select().where(cls.apply_url == url).get()

    @classmethod
    def remote_listing(cls) -> Iterable[Self]:
        return cls.listing().where(cls.remote == True)  # noqa: E712

    @classmethod
    def tags_listing(cls, tags: Iterable[str]) -> Iterable[Self]:
        tags = set(tags)
        return [
            job for job in cls.listing() if tags & set([tag.slug for tag in job.tags])
        ]

    @classmethod
    def internship_listing(cls) -> Iterable[Self]:
        return cls.tags_listing(["INTERNSHIP"])

    @classmethod
    def volunteering_listing(cls) -> Iterable[Self]:
        return cls.tags_listing(["VOLUNTEERING"])

    @classmethod
    def api_listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.posted_on.desc())

    def to_json_ld(self) -> str:
        return json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "JobPosting",
                "title": self.title,
                "url": self.effective_url,
                "description": (
                    "Pracovní nabídka pro začínající programátory nebo testery: "
                    + " — ".join([self.title, self.company_name, self.location])
                ),
                "datePosted": self.posted_on.isoformat(),
                "industry": "Informační technologie",
                "jobLocation": {
                    "@type": "Place",
                    "address": self.location,
                },
                "image": f"https://junior.guru/static/{self.company_logo_path}",
                "hiringOrganization": {
                    "@type": "Organization",
                    "name": self.company_name,
                    "logo": f"https://junior.guru/static/{self.company_logo_path}",
                },
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    def to_czechitas_api(self) -> dict[str, str | int | datetime | None]:
        return dict(
            **dict(
                title=self.title,
                company_name=self.company_name,
                url=self.effective_url,
                remote=self.remote,
                first_seen_at=datetime.combine(
                    self.posted_on, time(0, 0)
                ),  # datetime for backwards compatibility
                last_seen_at=None,  # not relevant anymore, equals to present moment
                lang=self.lang,
                juniority_score=None,  # won't expose publicly anymore
                source=None,  # use external IDs instead
            ),
            **{
                f"external_ids_{i}": value
                for i, value in columns(  # renamed elsewhere, but keeping backwards compatible
                    self.boards_ids, 10
                )
            },
            **{
                f"locations_{i}_name": (value["place"] if value else None)
                for i, value in columns(self.locations, 20)
            },
            **{
                f"locations_{i}_region": (value["region"] if value else None)
                for i, value in columns(self.locations, 20)
            },
            **{
                f"employment_types_{i}": value
                for i, value in columns(self.employment_types, 10)
            },
            **dict(
                description_html=self.description_html,
            ),
        )


class DiscordJob(BaseModel):
    title = CharField()
    author = ForeignKeyField(ClubUser, backref="list_jobs")
    posted_on = DateField(index=True)
    description_html = TextField()
    url = CharField(unique=True)
    upvotes_count = IntegerField()
    comments_count = IntegerField()

    @classmethod
    def get_by_url(cls, url) -> Self:
        return cls.select().where(cls.url == url).get()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(
            (cls.upvotes_count + cls.comments_count).desc(),
            cls.posted_on.desc(),
            cls.url.desc(),
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()


class JobStats(BaseModel):
    day = DateField(unique=True)
    scraped_count = IntegerField()
    discord_count = IntegerField()
    dropped_count = IntegerField()
    tech = JSONField(default=dict)

    @classmethod
    def deserialize(cls, line: str) -> Self | None:
        data = json.loads(line)
        data["day"] = date.fromisoformat(data["day"])
        return cls.add(**data)

    def serialize(self) -> str:
        data = model_to_dict(self, exclude=[self.__class__.id])
        data["day"] = self.day.isoformat()
        return json.dumps(data, ensure_ascii=False) + "\n"

    @classmethod
    def add(cls, **kwargs) -> None:
        try:
            cls.create(**kwargs)
        except IntegrityError:
            pass

    @classmethod
    def history(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.day)


def columns(values, columns_count):
    values = list(values or [])
    values_count = len(values)
    return enumerate(
        [values[i] if values_count > i else None for i in range(columns_count)]
    )
