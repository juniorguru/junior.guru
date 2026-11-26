from typing import Any

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_discord_job, create_job


@pytest.fixture
def context_options() -> dict[str, Any]:
    return {"java_script_enabled": False}


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


def test_without_js_discord_job_title_opens_thread(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.manual")
    requested_urls = []
    page.context.on("request", lambda request: requested_urls.append(request.url))
    with page.context.expect_page() as new_page_info:
        job.locator(".jobs-title-link").click()

    assert new_page_info.value.opener() == page
    assert "https://discord.com/channels/1/2/1" in requested_urls
    expect(job.locator(".jobs-club")).to_be_hidden()
