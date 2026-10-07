import re

from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_shows_all_jobs_without_filter(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="JavaScript Developer", tech_tags=["javascript"])
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.tagged")).to_have_count(2)
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)
    expect(page.locator(".jobs-empty")).to_be_hidden()


def test_filter_tags_are_revealed(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-filters [data-jobs-tag='python']")).to_be_visible()
    expect(page.locator(".jobs-noscript")).to_have_count(0)


def test_clicking_tag_filters_jobs(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="JavaScript Developer", tech_tags=["javascript"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Python Developer")
    expect(visible_jobs.locator("[data-jobs-tag='python']")).to_have_class(
        re.compile(r"\bmatching\b")
    )
    expect(page).to_have_url(re.compile(r"/jobs/\?technology=python$"))


def test_clicking_tag_again_resets_filter(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="JavaScript Developer", tech_tags=["javascript"])
    jobs_page()
    page.goto("/jobs/")

    tag = page.locator(".jobs-filters [data-jobs-tag='python']")
    tag.click()
    tag.click()

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)
    expect(page.locator(".jobs-item .jobs-tag.matching")).to_have_count(0)
    expect(page).to_have_url(re.compile(r"/jobs/$"))


def test_url_restores_filter(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="JavaScript Developer", tech_tags=["javascript"])
    jobs_page()
    page.goto("/jobs/?technology=javascript")

    expect(page.locator(".jobs-filters [data-jobs-tag='javascript']")).to_have_class(
        re.compile(r"\bactive\b")
    )
    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("JavaScript Developer")


def test_tags_of_same_type_are_alternatives(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="JavaScript Developer", tech_tags=["javascript"])
    create_job(title="Java Developer", tech_tags=["java"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    page.locator(".jobs-filters [data-jobs-tag='javascript']").click()

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)
    expect(page).to_have_url(re.compile(r"\?technology=javascript%7Cpython$"))


def test_no_matching_jobs_shows_empty_state(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"], remote=False)
    create_job(title="Remote Developer", tech_tags=["javascript"], remote=True)
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    page.locator(".jobs-filters [data-jobs-tag='remote']").click()

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(0)
    expect(page.locator(".jobs-empty")).to_be_visible()
