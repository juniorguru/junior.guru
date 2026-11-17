from itertools import chain

from jg.coop.models.job import RegionListing
from jg.coop.web.generators import (
    generate_employment_type_jobs_pages,
    generate_region_jobs_pages,
    generate_tech_jobs_pages,
    get_region_page_meta,
)


def test_jobs_listing_pages_have_unique_paths():
    paths = [
        document.path
        for document in chain(
            generate_region_jobs_pages(),
            generate_employment_type_jobs_pages(),
            generate_tech_jobs_pages(),
        )
    ]

    assert len(paths) == len(set(paths))


def test_get_region_page_meta_title_remote():
    region_listing = RegionListing(slug="remote", tag_slug="remote", name="Na dálku")
    meta = get_region_page_meta(region_listing, "Popis.")

    assert meta["title"].startswith("Remote ")


def test_get_region_page_meta_title_region():
    region_listing = RegionListing(slug="brno", tag_slug="brno", name="Brno")
    meta = get_region_page_meta(region_listing, "Popis.")

    assert ", Brno, " in meta["title"]


def test_get_region_page_meta_tag_slug():
    region_listing = RegionListing(
        slug="hradec-kralove", tag_slug="hradeckralove", name="Hradec Králové"
    )
    meta = get_region_page_meta(region_listing, "Popis.")

    assert meta["region_tag_slug"] == "hradeckralove"


def test_region_jobs_pages_paths():
    paths = {document.path for document in generate_region_jobs_pages()}

    assert {"jobs/remote.jinja", "jobs/hradec-kralove.jinja"} <= paths
