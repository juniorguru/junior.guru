from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Literal, Protocol, Self

from peewee import CharField, IntegerField
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.job import ListedJob, Tag, TagType


JOBS_DOC_PATH = "jobs.jinja"

ALL_JOBS_NAME = "Všechny nabídky"

LISTING_TYPES = [TagType.LOCATION, TagType.TECHNOLOGY, TagType.EMPLOYMENT]

NAV_HEADINGS = {
    TagType.LOCATION: "Místo",
    TagType.TECHNOLOGY: "Zaměření",
    TagType.EMPLOYMENT: "Další",
}

FILTERS = [
    (TagType.LOCATION, "Místo", "geo-alt", "Procházej všechna místa"),
    (TagType.EMPLOYMENT, "Úvazek", "hourglass-split", "Procházej i plné úvazky"),
    (TagType.TECHNOLOGY, "Nářadí", "tools", "Procházej všechny technologie"),
    (TagType.SOURCE, "Zdroj", "box-arrow-down", None),
]


JOBS_CLUB_POSITION = 4

JOBS_FORM_POSITION = 2


class JobsListingPage(BaseModel):
    """
    Standalone jobs listing page, e.g. /jobs/brno/, /jobs/python/, or /jobs/part-time/

    It shows jobs having any of its tags, and its type tells which filter it locks
    """

    position = IntegerField(unique=True)
    slug = CharField(unique=True)
    type = CharField()
    tag_slugs = JSONField()
    name = CharField()
    heading = CharField()
    title = CharField()
    description = CharField()
    lead = CharField(null=True)
    fallback_slug = CharField(null=True)

    @property
    def doc_path(self) -> str:
        return get_listing_doc_path(self.slug)

    def list_jobs(self) -> Iterable[ListedJob]:
        return ListedJob.tagged_listing(self.type, self.tag_slugs)

    @classmethod
    def get_by_slug(cls, slug: str) -> Self:
        return cls.get(cls.slug == slug)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.position)


class Listing(Protocol):
    slug: str
    type: str
    tag_slugs: list[str]
    name: str

    @property
    def doc_path(self) -> str: ...


class JobsNavLink(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    doc_path: str
    is_current: bool = False


class JobsNavGroup(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)

    type: TagType
    heading: str
    links: list[JobsNavLink]


class JobsFilterTag(Tag):
    is_fixed: bool = False


class JobsFilter(PydanticBaseModel):
    model_config = ConfigDict(frozen=True)

    type: TagType
    heading: str
    icon: str
    tags: list[JobsFilterTag]
    browse_all_text: str | None = None

    @property
    def selectable_slugs(self) -> list[str]:
        return [tag.slug for tag in self.tags if not tag.is_fixed]


def get_listing_doc_path(slug: str) -> str:
    """
    Path to the source document of a jobs listing page, as used by docs_url
    """
    return f"jobs/{slug}.jinja"


def get_listings_nav(
    listings: Iterable[Listing], current_doc_path: str | None = None
) -> list[JobsNavGroup]:
    """
    Groups links to listing pages by type, marking the current page

    The link to all jobs goes first to the last group.
    """
    links_by_type = {type: [] for type in LISTING_TYPES}
    for listing in listings:
        links_by_type[TagType(listing.type)].append((listing.name, listing.doc_path))
    links_by_type[LISTING_TYPES[-1]].insert(0, (ALL_JOBS_NAME, JOBS_DOC_PATH))
    return [
        JobsNavGroup(
            type=type,
            heading=NAV_HEADINGS[type],
            links=[
                JobsNavLink(
                    name=name,
                    doc_path=doc_path,
                    is_current=doc_path == current_doc_path,
                )
                for name, doc_path in links
            ],
        )
        for type, links in links_by_type.items()
    ]


def get_location_tags(listings: Iterable[Listing]) -> list[Tag]:
    """
    Lists tags of all location listings, in their order, e.g. #remote, #brno, …
    """
    return [
        Tag(slug=tag_slug, type=TagType.LOCATION)
        for listing in listings
        if listing.type == TagType.LOCATION
        for tag_slug in listing.tag_slugs
    ]


def get_jobs_filters(
    tags_by_type: dict[str, Sequence[Tag]],
    location_tags: Sequence[Tag],
    listing: Listing | None = None,
) -> dict[str, JobsFilter]:
    """
    Decides which tags to offer in each jobs filter, keyed by tag type

    Locations are always offered in full, other tags only if any job has them.
    The listing's own filter offers only the listing's tags. A single one is
    fixed, i.e. always active, several can be selected to narrow the listing.
    """
    filters = {}
    for type, heading, icon, browse_all_text in FILTERS:
        tags = location_tags if type == TagType.LOCATION else tags_by_type.get(type, [])
        is_listing_type = listing is not None and listing.type == type
        if is_listing_type:
            filter_tags = get_listing_filter_tags(listing, tags)
        else:
            filter_tags = [JobsFilterTag(slug=tag.slug, type=type) for tag in tags]
        filters[str(type)] = JobsFilter(
            type=type,
            heading=heading,
            icon=icon,
            tags=filter_tags,
            browse_all_text=browse_all_text if is_listing_type else None,
        )
    return filters


def get_listing_filter_tags(
    listing: Listing, tags: Iterable[Tag]
) -> list[JobsFilterTag]:
    if len(listing.tag_slugs) == 1:
        return [
            JobsFilterTag(slug=listing.tag_slugs[0], type=listing.type, is_fixed=True)
        ]
    return [
        JobsFilterTag(slug=tag.slug, type=listing.type)
        for tag in tags
        if tag.slug in listing.tag_slugs
    ]


@dataclass(frozen=True)
class JobsSlot:
    type: Literal["job", "manual_job", "form", "club"]
    job: Any = None


class HighlightableJob(Protocol):
    @property
    def is_highlighted(self) -> bool: ...


def get_jobs_slots(
    jobs: Iterable[HighlightableJob], manual_jobs: Iterable[Any]
) -> list[JobsSlot]:
    """
    Decides the order of items in a jobs listing

    Highlighted jobs go first, then manual jobs, then regular jobs. The GitHub
    profile check form comes after the second regular job, the club call
    to action after the fourth one. If there are fewer regular jobs, the boxes
    go at the end, so they're always present.
    """
    jobs = list(jobs)
    slots = [JobsSlot(type="job", job=job) for job in jobs if job.is_highlighted]
    slots.extend(JobsSlot(type="manual_job", job=job) for job in manual_jobs)
    regular_jobs = [job for job in jobs if not job.is_highlighted]
    boxes = {
        JOBS_FORM_POSITION: JobsSlot(type="form"),
        JOBS_CLUB_POSITION: JobsSlot(type="club"),
    }
    for position, job in enumerate(regular_jobs, start=1):
        slots.append(JobsSlot(type="job", job=job))
        if box := boxes.pop(position, None):
            slots.append(box)
    slots.extend(boxes[position] for position in sorted(boxes))
    return slots
