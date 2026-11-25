from collections.abc import Iterable
from pathlib import Path

import click
import yaml
from slugify import slugify

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.location import REGIONS
from jg.coop.lib.text import get_tag_slug
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.job import TagType
from jg.coop.models.jobs_listing import LISTING_TYPES, JobsListingPage


YAML_PATH = Path("src/jg/coop/data/jobs_listings.yml")


logger = loggers.from_path(__file__)


class JobsListingConfig(YAMLConfig):
    slug: str
    type: TagType
    tag_slugs: list[str]
    name: str
    heading: str
    title: str
    description: str
    lead: str | None = None
    fallback_slug: str | None = None


class RegionListingTemplate(YAMLConfig):
    heading: str
    title: str
    description: str
    fallback_slug: str | None = None


class JobsListingsConfig(YAMLConfig):
    listings: list[JobsListingConfig]
    region_listing: RegionListingTemplate


@cli.sync_command()
@click.option(
    "--path",
    default=YAML_PATH,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@db.connection_context()
def main(path: Path):
    JobsListingPage.drop_table()
    JobsListingPage.create_table()
    config = load_config(path)
    for position, listing in enumerate(build_listings(config, REGIONS), start=1):
        logger.info(f"#{position} {listing.slug}")
        JobsListingPage.create(position=position, **listing.model_dump())


def load_config(path: Path = YAML_PATH) -> JobsListingsConfig:
    return JobsListingsConfig(**yaml.safe_load(path.read_text()))


def build_listings(
    config: JobsListingsConfig, regions: Iterable[str]
) -> list[JobsListingConfig]:
    """
    Lists all listing pages, grouped by type, with regions after other locations
    """
    listings = [
        *config.listings,
        *(build_region_listing(config.region_listing, region) for region in regions),
    ]
    # The sort is stable, so within a type the order from the YAML is kept,
    # and generated regions go after the locations from the YAML
    return sorted(listings, key=lambda listing: LISTING_TYPES.index(listing.type))


def build_region_listing(
    template: RegionListingTemplate, region: str
) -> JobsListingConfig:
    region_nowrap = region.replace(" ", " ")
    return JobsListingConfig(
        slug=slugify(region),
        type=TagType.LOCATION,
        tag_slugs=[get_tag_slug(region)],
        name=region,
        heading=template.heading.format(region=region_nowrap),
        title=template.title.format(region=region),
        description=template.description.format(region=region),
        fallback_slug=template.fallback_slug,
    )
