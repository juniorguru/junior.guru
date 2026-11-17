import itertools
from collections.abc import Iterable, Sequence
from operator import attrgetter
from pathlib import Path
from typing import Protocol

import yaml
from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from slugify import slugify

from jg.coop.lib.location import REGIONS
from jg.coop.lib.text import get_tag_slug
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.job import Tag, TagType


JOBS_LISTINGS_YAML_PATH = Path(__file__).parent.parent / "data" / "jobs_listings.yml"

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


class Tagged(Protocol):
    @property
    def tags(self) -> list[Tag]: ...


class JobsListing(YAMLConfig):
    """
    Standalone jobs listing page, e.g. /jobs/brno/, /jobs/python/, or /jobs/part-time/

    It shows jobs having any of its tags, and its type tells which filter it locks
    """

    model_config = ConfigDict(frozen=True)

    slug: str
    type: TagType
    tag_slugs: list[str]
    name: str
    heading: str
    title: str
    description: str
    lead: str | None = None
    fallback_slug: str | None = None

    @property
    def doc_path(self) -> str:
        return get_listing_doc_path(self.slug)


class RegionListingTemplate(YAMLConfig):
    heading: str
    title: str
    description: str
    fallback_slug: str | None = None


class JobsListingsConfig(YAMLConfig):
    registry: list[JobsListing]
    region_listing: RegionListingTemplate


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


def load_jobs_listings(path: Path = JOBS_LISTINGS_YAML_PATH) -> list[JobsListing]:
    config = JobsListingsConfig(**yaml.safe_load(path.read_text()))
    return build_jobs_listings(config, REGIONS)


def build_jobs_listings(
    config: JobsListingsConfig, regions: Iterable[str]
) -> list[JobsListing]:
    """
    Lists all listing pages, grouped by type, with regions after other locations
    """
    listings = [
        *config.registry,
        *(build_region_listing(config.region_listing, region) for region in regions),
    ]
    # The sort is stable, so within a type the registry order is kept,
    # and generated regions go after the locations from the registry
    return sorted(listings, key=lambda listing: LISTING_TYPES.index(listing.type))


def build_region_listing(template: RegionListingTemplate, region: str) -> JobsListing:
    region_nowrap = region.replace(" ", " ")
    return JobsListing(
        slug=slugify(region),
        type=TagType.LOCATION,
        tag_slugs=[get_tag_slug(region)],
        name=region,
        heading=template.heading.format(region=region_nowrap),
        title=template.title.format(region=region),
        description=template.description.format(region=region),
        fallback_slug=template.fallback_slug,
    )


def get_listing_doc_path(slug: str) -> str:
    """
    Path to the source document of a jobs listing page, as used by docs_url
    """
    return f"jobs/{slug}.jinja"


def get_listings_nav(
    listings: Iterable[JobsListing], current_doc_path: str | None = None
) -> list[JobsNavGroup]:
    """
    Groups links to listing pages by type, marking the current page

    The link to all jobs goes first to the last group.
    """
    links_by_type = {type: [] for type in LISTING_TYPES}
    for listing in listings:
        links_by_type[listing.type].append((listing.name, listing.doc_path))
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


def get_location_tags(listings: Iterable[JobsListing]) -> list[Tag]:
    """
    Lists tags of all location listings, in their order, e.g. #remote, #brno, …
    """
    return [
        Tag(slug=tag_slug, type=TagType.LOCATION)
        for listing in listings
        if listing.type == TagType.LOCATION
        for tag_slug in listing.tag_slugs
    ]


def group_jobs_by_listing[TaggedT: Tagged](
    jobs: Iterable[TaggedT], listings: Iterable[JobsListing]
) -> dict[str, list[TaggedT]]:
    """
    Maps each listing slug to the jobs having any of the listing's tags
    """
    jobs = list(jobs)
    return {
        listing.slug: filter_by_tags(jobs, listing.tag_slugs) for listing in listings
    }


def filter_by_tags[TaggedT: Tagged](
    jobs: Iterable[TaggedT], tag_slugs: Iterable[str]
) -> list[TaggedT]:
    """
    Lists jobs having any of given tags, keeping their order
    """
    tag_slugs = set(tag_slugs)
    return [job for job in jobs if tag_slugs & {tag.slug for tag in job.tags}]


def group_tags_by_type(jobs: Iterable[Tagged]) -> dict[str, list[Tag]]:
    """
    Maps each tag type to sorted unique tags of given jobs
    """
    tags = sorted(
        set(itertools.chain.from_iterable(job.tags for job in jobs)),
        key=attrgetter("type", "slug"),
    )
    return {
        str(type).lower(): list(tags)
        for type, tags in itertools.groupby(tags, key=attrgetter("type"))
    }


def get_jobs_filters(
    tags_by_type: dict[str, Sequence[Tag]],
    location_tags: Sequence[Tag],
    listing: JobsListing | None = None,
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
    listing: JobsListing, tags: Iterable[Tag]
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


JOBS_LISTINGS = load_jobs_listings()

JOBS_LISTINGS_BY_SLUG = {listing.slug: listing for listing in JOBS_LISTINGS}
