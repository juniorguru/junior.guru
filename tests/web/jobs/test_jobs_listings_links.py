from collections.abc import Callable

import pytest
from playwright.sync_api import Page, expect
from web.conftest import docs_url_stub, render_string

from jg.coop.models.jobs_listing import JOBS_LISTINGS, get_listings_nav
from jg.coop.web.generators import generate_jobs_listing_pages


@pytest.fixture
def listings_page(serve: Callable[[str], None]) -> Callable:
    """
    Renders the section linking listing pages, as the jobs theme template does
    """

    def listings_page(current_doc_path: str | None = None) -> None:
        source = (
            "{% from 'macros.html' import jobs_listings with context %}"
            "{{ jobs_listings(nav_groups) }}"
        )
        context = {"nav_groups": get_listings_nav(JOBS_LISTINGS, current_doc_path)}
        serve(render_string(source, context, "/jobs/"))

    return listings_page


def test_links_to_all_generated_listing_pages(page: Page, listings_page):
    listings_page()
    page.goto("/jobs/")

    hrefs = page.locator(".jobs-listings-link").evaluate_all(
        "links => links.map(link => link.getAttribute('href'))"
    )
    expected_hrefs = {
        docs_url_stub(document.path) for document in generate_jobs_listing_pages()
    } | {"/jobs/"}
    assert set(hrefs) == expected_hrefs


def test_current_listing_is_marked(page: Page, listings_page):
    listings_page("jobs/brno.jinja")
    page.goto("/jobs/")

    expect(page.locator(".jobs-listings-link[aria-current='page']")).to_have_text(
        "Brno"
    )
