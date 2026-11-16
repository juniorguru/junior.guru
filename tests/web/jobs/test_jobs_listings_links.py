import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_links_to_all_listing_pages(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    links = page.locator(".jobs-listings-link")
    expect(links.filter(has_text="Na dálku")).to_have_count(1)
    expect(links.filter(has_text="Brno")).to_have_count(1)
    expect(links.filter(has_text="Python")).to_have_count(1)


@pytest.mark.parametrize(
    "url, name",
    [
        ("/jobs/remote/", "Na dálku"),
        ("/jobs/brno/", "Brno"),
        ("/jobs/python/", "Python"),
    ],
)
def test_current_listing_is_marked(page: Page, jobs_page, url: str, name: str):
    create_job(title="Python Developer", regions=["Brno"])
    jobs_page(url)
    page.goto(url)

    expect(page.locator(".jobs-listings-link[aria-current='page']")).to_have_text(name)
