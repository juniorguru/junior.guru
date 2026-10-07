from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, Page, expect
from web.conftest import BASE_URL
from web.helpers import create_job


@pytest.fixture
def page(browser: Browser) -> Generator[Page]:
    context = browser.new_context(base_url=BASE_URL, java_script_enabled=False)
    page = context.new_page()
    yield page
    context.close()


def test_without_js_all_jobs_are_listed(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="Java Developer", tech_tags=["java"])
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)
    expect(page.locator(".jobs-empty")).to_be_hidden()


def test_without_js_filters_show_error(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-noscript").first).to_be_visible()
    expect(page.locator(".jobs-filters [data-jobs-tag='python']")).to_be_hidden()


def test_without_js_jobs_are_closed_links(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    expect(job.locator(".jobs-title-link")).to_be_visible()
    expect(job.locator(".jobs-title-link")).to_have_attribute(
        "href", "https://example.com/jobs/1"
    )
    expect(job.locator(".jobs-actions")).to_be_hidden()
    expect(job.locator(".jobs-company")).to_be_hidden()
