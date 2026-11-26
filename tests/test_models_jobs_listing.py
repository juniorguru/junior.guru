from collections.abc import Generator
from types import SimpleNamespace

import pytest

from jg.coop.models.base import SqliteDatabase
from jg.coop.models.job import JobTag, ListedJob, Tag, TagType
from jg.coop.models.jobs_listing import (
    JobsListingPage,
    JobsSlot,
    get_jobs_filters,
    get_jobs_slots,
    get_listings_nav,
    get_location_tags,
)

from testing_utils import prepare_test_db


@pytest.fixture
def test_db() -> Generator[SqliteDatabase]:
    yield from prepare_test_db([JobsListingPage, ListedJob, JobTag])


def create_listing(**kwargs) -> SimpleNamespace:
    listing = SimpleNamespace(
        **{
            "slug": "python",
            "type": TagType.TECHNOLOGY,
            "tag_slugs": ["python"],
            "name": "Python",
        }
        | kwargs
    )
    listing.doc_path = f"jobs/{listing.slug}.jinja"
    return listing


def create_listing_page(position: int, **kwargs) -> JobsListingPage:
    return JobsListingPage.create(
        **{
            "position": position,
            "slug": f"listing-{position}",
            "type": "technology",
            "tag_slugs": ["python"],
            "name": "Python",
            "heading": "Heading",
            "title": "Title",
            "description": "Description",
        }
        | kwargs
    )


def test_listing_page_doc_path():
    page = JobsListingPage(slug="hradec-kralove")

    assert page.doc_path == "jobs/hradec-kralove.jinja"


def test_listing_pages_sorted_by_position(test_db: SqliteDatabase):
    create_listing_page(2, slug="b")
    create_listing_page(1, slug="a")

    assert [page.slug for page in JobsListingPage.listing()] == ["a", "b"]


def test_listing_page_get_by_slug(test_db: SqliteDatabase):
    create_listing_page(1, slug="brno")

    assert JobsListingPage.get_by_slug("brno").position == 1


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


def test_get_listings_nav_headings():
    nav = get_listings_nav([])

    assert [group.heading for group in nav] == ["Místo", "Zaměření", "Další"]


def test_get_listings_nav_accepts_type_as_string():
    nav = get_listings_nav([create_listing(type="location", name="Brno")])

    assert [link.name for link in nav[0].links] == ["Brno"]


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
        create_listing(slug="brno", type="location", tag_slugs=["brno"]),
    ]

    assert get_location_tags(listings) == [
        Tag(slug="remote", type=TagType.LOCATION),
        Tag(slug="brno", type=TagType.LOCATION),
    ]


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
    listing = create_listing(slug="brno", type="location", tag_slugs=["brno"])
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


def create_job(name: str, is_highlighted: bool = False) -> SimpleNamespace:
    return SimpleNamespace(name=name, is_highlighted=is_highlighted)


def format_slots(slots: list[JobsSlot]) -> list[str]:
    return [slot.job.name if slot.job else slot.type for slot in slots]


@pytest.mark.parametrize(
    "jobs, manual_jobs, expected",
    [
        pytest.param([], [], ["club"], id="nothing"),
        pytest.param([], ["m1", "m2"], ["m1", "m2", "club"], id="only manual"),
        pytest.param(["r1"], [], ["r1", "club"], id="one regular"),
        pytest.param(
            ["r1", "r2", "r3", "r4", "r5", "r6", "r7"],
            [],
            ["r1", "r2", "r3", "club", "r4", "r5", "r6", "r7"],
            id="only regular",
        ),
        pytest.param(
            ["r1", "r2", "r3", "r4", "r5", "r6", "r7"],
            ["m1", "m2"],
            ["r1", "r2", "r3", "m1", "r4", "r5", "m2", "r6", "r7", "club"],
            id="regular and manual",
        ),
        pytest.param(
            ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"],
            ["m1"],
            ["r1", "r2", "r3", "m1", "r4", "r5", "club", "r6", "r7", "r8", "r9"],
            id="manual run out",
        ),
        pytest.param(
            ["r1", "r2", "r3"],
            ["m1", "m2", "m3"],
            ["r1", "r2", "r3", "m1", "m2", "m3", "club"],
            id="regular run out",
        ),
    ],
)
def test_get_jobs_slots(jobs: list[str], manual_jobs: list[str], expected: list[str]):
    slots = get_jobs_slots(
        [create_job(name) for name in jobs],
        [create_job(name) for name in manual_jobs],
    )

    assert format_slots(slots) == expected


def test_get_jobs_slots_highlighted_first():
    jobs = [
        create_job("r1"),
        create_job("h1", is_highlighted=True),
        create_job("r2"),
        create_job("r3"),
        create_job("h2", is_highlighted=True),
    ]
    slots = get_jobs_slots(jobs, [create_job("m1")])

    assert format_slots(slots) == ["h1", "h2", "r1", "r2", "r3", "m1", "club"]
