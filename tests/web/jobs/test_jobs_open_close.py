import re

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
