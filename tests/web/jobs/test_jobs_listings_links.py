from collections.abc import Callable

import pytest
from peewee import SqliteDatabase
from playwright.sync_api import Page, expect
from web.conftest import docs_url_stub, render_string
from web.helpers import create_listing_pages

from jg.coop.models.jobs_listing import get_listings_nav


@pytest.fixture
def listings_page(test_db: SqliteDatabase, serve: Callable[[str], None]) -> Callable:
    """
    Renders the section linking listing pages, as the jobs theme template does
    """

    def listings_page(current_doc_path: str | None = None) -> list[str]:
        listings = create_listing_pages()
        source = (
            "{% from 'macros.html' import jobs_listings with context %}"
            "{{ jobs_listings(nav_groups) }}"
        )
        context = {"nav_groups": get_listings_nav(listings, current_doc_path)}
        serve(render_string(source, context, "/jobs/"))
        return [listing.doc_path for listing in listings]

    return listings_page


def test_links_to_all_listing_pages(page: Page, listings_page):
    doc_paths = listings_page()
    page.goto("/jobs/")

    hrefs = page.locator(".jobs-listings-link").evaluate_all(
        "links => links.map(link => link.getAttribute('href'))"
    )
    assert set(hrefs) == {docs_url_stub(path) for path in doc_paths} | {"/jobs/"}


def test_current_listing_is_marked(page: Page, listings_page):
    listings_page("jobs/brno.jinja")
    page.goto("/jobs/")

    expect(page.locator(".jobs-listings-link[aria-current='page']")).to_have_text(
        "Brno"
    )
