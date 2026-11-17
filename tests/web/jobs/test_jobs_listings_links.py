from collections.abc import Callable
from itertools import chain

import pytest
from playwright.sync_api import Page, expect
from web.conftest import docs_url_stub, render_string

from jg.coop.models.job import JOBS_OTHER_LINKS, REGION_LISTINGS, TECH_LISTINGS
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

    def listings_page(current_doc_path: str | None = None) -> None:
        source = (
            "{% from 'macros.html' import jobs_listings with context %}"
            "{{ jobs_listings(region_listings, tech_listings, other_links,"
            " current_doc_path=current_doc_path) }}"
        )
        context = {
            "region_listings": REGION_LISTINGS,
            "tech_listings": TECH_LISTINGS,
            "other_links": JOBS_OTHER_LINKS,
            "current_doc_path": current_doc_path,
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


@pytest.mark.parametrize(
    "current_doc_path, name",
    [
        ("jobs.jinja", "Všechny nabídky"),
        ("jobs/remote.jinja", "Na dálku"),
        ("jobs/brno.jinja", "Brno"),
        ("jobs/python.jinja", "Python"),
        ("jobs/part-time.jinja", "Brigády a\u00a0stáže"),
    ],
)
def test_current_listing_is_marked(
    page: Page, listings_page, current_doc_path: str, name: str
):
    listings_page(current_doc_path)
    page.goto("/jobs/")

    expect(page.locator(".jobs-listings-link[aria-current='page']")).to_have_text(name)
