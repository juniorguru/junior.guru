from collections.abc import Callable

import pytest
from playwright.sync_api import Page, expect
from web.conftest import render_string

from jg.coop.models.job import REGION_LISTINGS, TECH_LISTINGS


@pytest.fixture
def listings_page(serve: Callable[[str], None]) -> Callable:
    """
    Renders the section linking listing pages, as the jobs theme template does
    """

    def listings_page(
        current_region_tag_slug: str | None = None,
        current_tech_listing_slug: str | None = None,
    ) -> None:
        source = (
            "{% from 'macros.html' import jobs_listings with context %}"
            "{{ jobs_listings(region_listings, tech_listings,"
            " current_region_tag_slug=current_region_tag_slug,"
            " current_tech_listing_slug=current_tech_listing_slug) }}"
        )
        context = {
            "region_listings": REGION_LISTINGS,
            "tech_listings": TECH_LISTINGS,
            "current_region_tag_slug": current_region_tag_slug,
            "current_tech_listing_slug": current_tech_listing_slug,
        }
        serve(render_string(source, context, "/jobs/"))

    return listings_page


def test_links_to_listing_pages(page: Page, listings_page):
    listings_page()
    page.goto("/jobs/")

    links = page.locator(".jobs-listings-link")
    expect(links.filter(has_text="Na dálku")).to_have_count(1)
    expect(links.filter(has_text="Brno")).to_have_count(1)
    expect(links.filter(has_text="Python")).to_have_count(1)


def test_no_current_listing_on_main_page(page: Page, listings_page):
    listings_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-listings-link[aria-current='page']")).to_have_count(0)


@pytest.mark.parametrize(
    "current_region_tag_slug, current_tech_listing_slug, name",
    [
        ("remote", None, "Na dálku"),
        ("brno", None, "Brno"),
        (None, "python", "Python"),
    ],
)
def test_current_listing_is_marked(
    page: Page,
    listings_page,
    current_region_tag_slug: str | None,
    current_tech_listing_slug: str | None,
    name: str,
):
    listings_page(current_region_tag_slug, current_tech_listing_slug)
    page.goto("/jobs/")

    expect(page.locator(".jobs-listings-link[aria-current='page']")).to_have_text(name)
