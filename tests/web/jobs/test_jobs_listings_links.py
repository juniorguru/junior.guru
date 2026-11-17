from collections.abc import Callable
from itertools import chain

import pytest
from playwright.sync_api import Page, expect
from web.conftest import docs_url_stub, render_string

from jg.coop.models.job import REGION_LISTINGS, TECH_LISTINGS
from jg.coop.web.generators import (
    generate_employment_type_jobs_pages,
    generate_region_jobs_pages,
    generate_tech_jobs_pages,
)


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


@pytest.mark.parametrize(
    "name, href",
    [
        ("Na dálku", "/jobs/remote/"),
        ("Hradec Králové", "/jobs/hradec-kralove/"),
        ("Ústí nad Labem", "/jobs/usti-nad-labem/"),
        ("Python", "/jobs/python/"),
        ("C#\u00a0a\u00a0.NET", "/jobs/csharp/"),
        ("Všechny nabídky", "/jobs/"),
        ("Brigády a\u00a0stáže", "/jobs/part-time/"),
    ],
)
def test_links_to_listing_pages(page: Page, listings_page, name: str, href: str):
    listings_page()
    page.goto("/jobs/")

    link = page.locator(".jobs-listings-link", has_text=name)
    expect(link).to_have_attribute("href", href)


def test_links_to_all_generated_listing_pages(page: Page, listings_page):
    listings_page()
    page.goto("/jobs/")

    hrefs = page.locator(".jobs-listings-link").evaluate_all(
        "links => links.map(link => link.getAttribute('href'))"
    )
    expected_hrefs = {
        docs_url_stub(document.path)
        for document in chain(
            generate_region_jobs_pages(),
            generate_employment_type_jobs_pages(),
            generate_tech_jobs_pages(),
        )
    } | {"/jobs/"}
    assert set(hrefs) == expected_hrefs


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
