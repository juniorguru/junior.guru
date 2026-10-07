import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_jobs_are_closed_initially(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    expect(job).not_to_have_class(re.compile(r"\bopen\b"))
    expect(job.locator(".jobs-title-link")).to_be_visible()
    expect(job.locator(".jobs-open")).to_be_visible()
    expect(job.locator(".jobs-close")).to_be_hidden()
    expect(job.locator(".jobs-actions")).to_be_hidden()
    expect(job.locator(".jobs-company")).to_be_hidden()


def test_clicking_title_opens_job(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    job.locator(".jobs-title-link").click()

    expect(page).to_have_url(re.compile(r"/jobs/$"))
    assert len(page.context.pages) == 1
    expect(job).to_have_class(re.compile(r"\bopen\b"))
    expect(job.locator(".jobs-title-link")).to_be_hidden()
    expect(job.locator(".jobs-open")).to_be_hidden()
    expect(job.locator(".jobs-title-text")).to_be_visible()
    expect(job.locator(".jobs-title-text")).to_have_text("Python Developer")
    expect(job.locator(".jobs-close")).to_be_visible()
    expect(job.locator(".jobs-actions")).to_be_visible()
    expect(job.locator(".jobs-company")).to_be_visible()


def test_clicking_close_closes_job(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    job.locator(".jobs-title-link").click()
    job.locator(".jobs-close").click()

    expect(job).not_to_have_class(re.compile(r"\bopen\b"))
    expect(job.locator(".jobs-title-link")).to_be_visible()
    expect(job.locator(".jobs-open")).to_be_visible()
    expect(job.locator(".jobs-title-text")).to_be_hidden()
    expect(job.locator(".jobs-close")).to_be_hidden()
    expect(job.locator(".jobs-actions")).to_be_hidden()
    expect(job.locator(".jobs-company")).to_be_hidden()


def test_opening_one_job_leaves_others_closed(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_job(title="Java Developer")
    jobs_page()
    page.goto("/jobs/")

    jobs = page.locator(".jobs-item.tagged")
    jobs.nth(0).locator(".jobs-title-link").click()

    expect(jobs.nth(0)).to_have_class(re.compile(r"\bopen\b"))
    expect(jobs.nth(1)).not_to_have_class(re.compile(r"\bopen\b"))
    expect(jobs.nth(1).locator(".jobs-actions")).to_be_hidden()


def test_subscribe_box_hides_after_click(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    subscribe = page.locator(".jobs-subscribe")
    expect(subscribe).to_be_visible()
    subscribe.click()

    expect(subscribe).to_be_hidden()


def test_clicking_anywhere_on_job_opens_it(page: Page, jobs_page):
    create_job(title="Python Developer", company_name="Kuře Žluté, s.r.o.")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    company = job.locator(".jobs-info").get_by_text("Kuře Žluté, s.r.o.")
    box = company.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

    expect(job).to_have_class(re.compile(r"\bopen\b"))
    expect(page).to_have_url(re.compile(r"/jobs/$"))


def test_open_job_links_are_clickable(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    job.locator(".jobs-title-link").click()
    requested_urls = []
    page.context.on("request", lambda request: requested_urls.append(request.url))
    with page.context.expect_page() as new_page_info:
        # the fixed subscribe box covers the bottom of this short test page
        job.locator(".jobs-action-button.continue").press("Enter")

    assert new_page_info.value.opener() == page
    assert "https://example.com/jobs/1" in requested_urls
    expect(job).to_have_class(re.compile(r"\bopen\b"))


@pytest.mark.xfail(
    reason="Bug: clicks with a modifier key open the job instead of a new tab",
    strict=True,
    raises=AssertionError,
)
def test_modifier_click_on_title_opens_new_tab(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.tagged")
    job.locator(".jobs-title-link").click(modifiers=["ControlOrMeta"])

    expect(job).not_to_have_class(re.compile(r"\bopen\b"))
    expect(job.locator(".jobs-actions")).to_be_hidden()
