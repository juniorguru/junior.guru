import re

from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_remote_page_shows_only_remote_jobs(page: Page, jobs_page):
    create_job(title="Remote Developer", remote=True)
    create_job(title="Brno Developer", regions=["Brno"])
    jobs_page("/jobs/remote/")
    page.goto("/jobs/remote/")

    remote_tag = page.locator(".jobs-filters [data-jobs-tag='remote']")
    expect(remote_tag).to_have_count(1)
    expect(remote_tag).to_have_class(re.compile(r"\bactive\b"))
    jobs = page.locator(".jobs-item.tagged")
    expect(jobs).to_have_count(1)
    expect(jobs).to_contain_text("Remote Developer")
    expect(page).to_have_url(re.compile(r"/jobs/remote/$"))


def test_remote_page_with_other_filters(page: Page, jobs_page):
    create_job(title="Remote Python", remote=True, tech_tags=["python"])
    create_job(title="Remote Java", remote=True, tech_tags=["java"])
    jobs_page("/jobs/remote/")
    page.goto("/jobs/remote/")

    page.locator(".jobs-filters [data-jobs-tag='java']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Remote Java")
    expect(page).to_have_url(re.compile(r"/jobs/remote/\?technology=java$"))


def test_remote_page_empty_state_does_not_suggest_remote(page: Page, jobs_page):
    create_job(
        title="Remote Python",
        remote=True,
        tech_tags=["python"],
        employment_types=["fulltime"],
    )
    create_job(
        title="Remote Java",
        remote=True,
        tech_tags=["java"],
        employment_types=["internship"],
    )
    jobs_page("/jobs/remote/")
    page.goto("/jobs/remote/?technology=java&employment=fulltime")

    empty = page.locator(".jobs-empty")
    expect(empty).to_be_visible()
    expect(empty).not_to_contain_text("#remote")
