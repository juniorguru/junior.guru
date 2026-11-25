from types import SimpleNamespace

import pytest

from jg.coop.models.job import Tag, TagType
from jg.coop.models.jobs_listing import (
    JOBS_LISTINGS,
    JOBS_LISTINGS_BY_SLUG,
    JobsListing,
    JobsListingsConfig,
    RegionListingTemplate,
    build_jobs_listings,
    build_region_listing,
    filter_by_tags,
    get_jobs_filters,
    get_listings_nav,
    get_location_tags,
    group_jobs_by_listing,
    group_tags_by_type,
)


def create_listing(**kwargs) -> JobsListing:
    return JobsListing(
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


def create_job(*tags: Tag) -> SimpleNamespace:
    return SimpleNamespace(tags=list(tags))


REGION_TEMPLATE = RegionListingTemplate(
    heading="Práce: {region}",
    title="Práce, {region}",
    description="Popis {region}",
    fallback_slug="remote",
)


def test_jobs_listings_have_unique_slugs():
    slugs = [listing.slug for listing in JOBS_LISTINGS]

    assert len(slugs) == len(set(slugs))


def test_jobs_listings_fallbacks_exist():
    fallback_slugs = {listing.fallback_slug for listing in JOBS_LISTINGS} - {None}

    assert fallback_slugs <= set(JOBS_LISTINGS_BY_SLUG)


def test_jobs_listings_regions_fall_back_to_remote():
    region_listings = [
        listing
        for listing in JOBS_LISTINGS
        if listing.type == TagType.LOCATION and listing.slug != "remote"
    ]

    assert {listing.fallback_slug for listing in region_listings} == {"remote"}


def test_jobs_listings_start_with_remote():
    assert JOBS_LISTINGS[0].slug == "remote"


def test_jobs_listings_include_regions():
    assert {"brno", "hradec-kralove", "usti-nad-labem"} <= set(JOBS_LISTINGS_BY_SLUG)


def test_build_jobs_listings_keeps_yaml_order_first_within_type():
    config = JobsListingsConfig(
        listings=[create_listing(slug="remote", type=TagType.LOCATION)],
        region_listing=REGION_TEMPLATE,
    )
    listings = build_jobs_listings(config, ["Brno", "Praha"])

    assert [listing.slug for listing in listings] == ["remote", "brno", "praha"]


def test_build_jobs_listings_groups_by_type():
    config = JobsListingsConfig(
        listings=[
            create_listing(slug="part-time", type=TagType.EMPLOYMENT),
            create_listing(slug="python", type=TagType.TECHNOLOGY),
            create_listing(slug="remote", type=TagType.LOCATION),
        ],
        region_listing=REGION_TEMPLATE,
    )
    listings = build_jobs_listings(config, ["Brno"])

    assert [listing.slug for listing in listings] == [
        "remote",
        "brno",
        "python",
        "part-time",
    ]


def test_build_region_listing():
    listing = build_region_listing(REGION_TEMPLATE, "Hradec Králové")

    assert listing == JobsListing(
        slug="hradec-kralove",
        type=TagType.LOCATION,
        tag_slugs=["hradeckralove"],
        name="Hradec Králové",
        heading="Práce: Hradec Králové",
        title="Práce, Hradec Králové",
        description="Popis Hradec Králové",
        fallback_slug="remote",
    )


def test_listing_doc_path():
    assert create_listing(slug="hradec-kralove").doc_path == "jobs/hradec-kralove.jinja"


def test_get_listings_nav_groups():
    listings = [
        create_listing(slug="remote", type=TagType.LOCATION, name="Na dálku"),
        create_listing(slug="python", type=TagType.TECHNOLOGY, name="Python"),
        create_listing(slug="part-time", type=TagType.EMPLOYMENT, name="Brigády"),
    ]
    nav = get_listings_nav(listings)

    assert [[link.name for link in group.links] for group in nav] == [
        ["Na dálku"],
        ["Python"],
        ["Všechny nabídky", "Brigády"],
    ]


@pytest.mark.parametrize(
    "current_doc_path, expected",
    [
        ("jobs.jinja", ["Všechny nabídky"]),
        ("jobs/python.jinja", ["Python"]),
        ("jobs/part-time.jinja", ["Brigády"]),
        ("index.jinja", []),
        (None, []),
    ],
)
def test_get_listings_nav_marks_current(current_doc_path: str | None, expected):
    listings = [
        create_listing(slug="python", type=TagType.TECHNOLOGY, name="Python"),
        create_listing(slug="part-time", type=TagType.EMPLOYMENT, name="Brigády"),
    ]
    nav = get_listings_nav(listings, current_doc_path)

    assert [
        link.name for group in nav for link in group.links if link.is_current
    ] == expected


def test_get_location_tags():
    listings = [
        create_listing(slug="remote", type=TagType.LOCATION, tag_slugs=["remote"]),
        create_listing(slug="python", type=TagType.TECHNOLOGY, tag_slugs=["python"]),
        create_listing(slug="brno", type=TagType.LOCATION, tag_slugs=["brno"]),
    ]

    assert get_location_tags(listings) == [
        Tag(slug="remote", type=TagType.LOCATION),
        Tag(slug="brno", type=TagType.LOCATION),
    ]


def test_group_jobs_by_listing():
    js = create_job(Tag(slug="javascript", type=TagType.TECHNOLOGY))
    ts = create_job(Tag(slug="typescript", type=TagType.TECHNOLOGY))
    python = create_job(Tag(slug="python", type=TagType.TECHNOLOGY))
    listings = [
        create_listing(slug="javascript", tag_slugs=["javascript", "typescript"]),
        create_listing(slug="java", tag_slugs=["java"]),
    ]

    assert group_jobs_by_listing([js, python, ts], listings) == {
        "javascript": [js, ts],
        "java": [],
    }


def test_filter_by_tags():
    python = create_job(Tag(slug="python", type=TagType.TECHNOLOGY))
    java = create_job(Tag(slug="java", type=TagType.TECHNOLOGY))
    untagged = create_job()

    assert filter_by_tags([python, java, untagged], ["python", "ruby"]) == [python]


def test_group_tags_by_type():
    jobs = [
        create_job(
            Tag(slug="python", type=TagType.TECHNOLOGY),
            Tag(slug="brno", type=TagType.LOCATION),
        ),
        create_job(
            Tag(slug="java", type=TagType.TECHNOLOGY),
            Tag(slug="python", type=TagType.TECHNOLOGY),
        ),
    ]

    assert group_tags_by_type(jobs) == {
        "location": [Tag(slug="brno", type=TagType.LOCATION)],
        "technology": [
            Tag(slug="java", type=TagType.TECHNOLOGY),
            Tag(slug="python", type=TagType.TECHNOLOGY),
        ],
    }


LOCATION_TAGS = [
    Tag(slug="remote", type=TagType.LOCATION),
    Tag(slug="brno", type=TagType.LOCATION),
]

TAGS_BY_TYPE = {
    "employment": [
        Tag(slug="fulltime", type=TagType.EMPLOYMENT),
        Tag(slug="internship", type=TagType.EMPLOYMENT),
    ],
    "technology": [
        Tag(slug="java", type=TagType.TECHNOLOGY),
        Tag(slug="javascript", type=TagType.TECHNOLOGY),
        Tag(slug="python", type=TagType.TECHNOLOGY),
    ],
}


def test_get_jobs_filters_types():
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS)

    assert list(filters) == ["location", "employment", "technology", "source"]


def test_get_jobs_filters_offers_all_locations():
    filters = get_jobs_filters({}, LOCATION_TAGS)

    assert filters["location"].selectable_slugs == ["remote", "brno"]


def test_get_jobs_filters_offers_tags_of_jobs():
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS)

    assert filters["technology"].selectable_slugs == ["java", "javascript", "python"]


def test_get_jobs_filters_without_listing_has_no_browse_all_link():
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS)

    assert all(not f.browse_all_text for f in filters.values())


def test_get_jobs_filters_fixes_single_listing_tag():
    listing = create_listing(slug="brno", type=TagType.LOCATION, tag_slugs=["brno"])
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS, listing)

    assert [(tag.slug, tag.is_fixed) for tag in filters["location"].tags] == [
        ("brno", True)
    ]


def test_get_jobs_filters_narrows_multiple_listing_tags():
    listing = create_listing(
        slug="part-time",
        type=TagType.EMPLOYMENT,
        tag_slugs=["internship", "parttime", "volunteering"],
    )
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS, listing)

    assert filters["employment"].selectable_slugs == ["internship"]


def test_get_jobs_filters_keeps_other_types_for_listing():
    listing = create_listing(slug="python", tag_slugs=["python"])
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS, listing)

    assert filters["location"].selectable_slugs == ["remote", "brno"]


def test_get_jobs_filters_browse_all_link_for_listing_type():
    listing = create_listing(slug="python", tag_slugs=["python"])
    filters = get_jobs_filters(TAGS_BY_TYPE, LOCATION_TAGS, listing)

    assert [type for type, f in filters.items() if f.browse_all_text] == ["technology"]


@pytest.mark.parametrize(
    "heading, name, doc_path",
    [
        ("Místo", "Na dálku", "jobs/remote.jinja"),
        ("Místo", "Hradec Králové", "jobs/hradec-kralove.jinja"),
        ("Místo", "Ústí nad Labem", "jobs/usti-nad-labem.jinja"),
        ("Zaměření", "Python", "jobs/python.jinja"),
        ("Zaměření", "C# a .NET", "jobs/csharp.jinja"),
        ("Další", "Všechny nabídky", "jobs.jinja"),
        ("Další", "Brigády a stáže", "jobs/part-time.jinja"),
    ],
)
def test_jobs_listings_nav_links(heading: str, name: str, doc_path: str):
    links = {
        (group.heading, link.name): link.doc_path
        for group in get_listings_nav(JOBS_LISTINGS)
        for link in group.links
    }

    assert links[(heading, name)] == doc_path
