import pytest

from jg.coop.lib.location import REGIONS
from jg.coop.models.job import TagType
from jg.coop.sync.jobs_listing_pages import (
    JobsListingConfig,
    JobsListingsConfig,
    RegionListingTemplate,
    build_listings,
    build_region_listing,
    load_config,
)


REGION_TEMPLATE = RegionListingTemplate(
    heading="Práce: {region}",
    title="Práce, {region}",
    description="Popis {region}",
    fallback_slug="remote",
)


def create_listing(**kwargs) -> JobsListingConfig:
    return JobsListingConfig(
        **{
            "slug": "python",
            "type": TagType.TECHNOLOGY,
            "tag_slugs": ["python"],
            "name": "Python",
            "heading": "Heading",
            "title": "Title",
            "description": "Description",
        }
        | kwargs
    )


@pytest.fixture(scope="module")
def listings() -> list[JobsListingConfig]:
    return build_listings(load_config(), REGIONS)


def test_listings_have_unique_slugs(listings: list[JobsListingConfig]):
    slugs = [listing.slug for listing in listings]

    assert len(slugs) == len(set(slugs))


def test_listings_fallbacks_exist(listings: list[JobsListingConfig]):
    fallback_slugs = {listing.fallback_slug for listing in listings} - {None}

    assert fallback_slugs <= {listing.slug for listing in listings}


def test_listings_regions_fall_back_to_remote(listings: list[JobsListingConfig]):
    region_listings = [
        listing
        for listing in listings
        if listing.type == TagType.LOCATION and listing.slug != "remote"
    ]

    assert {listing.fallback_slug for listing in region_listings} == {"remote"}


def test_listings_start_with_remote(listings: list[JobsListingConfig]):
    assert listings[0].slug == "remote"


def test_listings_include_regions(listings: list[JobsListingConfig]):
    slugs = {listing.slug for listing in listings}

    assert {"brno", "hradec-kralove", "usti-nad-labem"} <= slugs


def test_listings_names_of_tech_and_employment(listings: list[JobsListingConfig]):
    names = {listing.slug: listing.name for listing in listings}

    assert (names["csharp"], names["part-time"]) == (
        "C# a .NET",
        "Brigády a stáže",
    )


def test_build_listings_keeps_yaml_order_first_within_type():
    config = JobsListingsConfig(
        listings=[create_listing(slug="remote", type=TagType.LOCATION)],
        region_listing=REGION_TEMPLATE,
    )
    listings = build_listings(config, ["Brno", "Praha"])

    assert [listing.slug for listing in listings] == ["remote", "brno", "praha"]


def test_build_listings_groups_by_type():
    config = JobsListingsConfig(
        listings=[
            create_listing(slug="part-time", type=TagType.EMPLOYMENT),
            create_listing(slug="python", type=TagType.TECHNOLOGY),
            create_listing(slug="remote", type=TagType.LOCATION),
        ],
        region_listing=REGION_TEMPLATE,
    )
    listings = build_listings(config, ["Brno"])

    assert [listing.slug for listing in listings] == [
        "remote",
        "brno",
        "python",
        "part-time",
    ]


def test_build_region_listing():
    listing = build_region_listing(REGION_TEMPLATE, "Hradec Králové")

    assert listing == JobsListingConfig(
        slug="hradec-kralove",
        type=TagType.LOCATION,
        tag_slugs=["hradeckralove"],
        name="Hradec Králové",
        heading="Práce: Hradec Králové",
        title="Práce, Hradec Králové",
        description="Popis Hradec Králové",
        fallback_slug="remote",
    )
