import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_discord_job, create_job


def test_tags_of_different_types_must_all_match(page: Page, jobs_page):
    create_job(
        title="Python Internship", tech_tags=["python"], employment_types=["internship"]
    )
    create_job(
        title="Python Full-time", tech_tags=["python"], employment_types=["fulltime"]
    )
    create_job(
        title="Java Internship", tech_tags=["java"], employment_types=["internship"]
    )
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    page.locator(".jobs-filters [data-jobs-tag='internship']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Python Internship")


def test_filter_by_employment_type(page: Page, jobs_page):
    create_job(title="Internship", employment_types=["internship"])
    create_job(title="Full-time", employment_types=["fulltime"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='internship']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Internship")
    expect(page).to_have_url(re.compile(r"/jobs/\?employment=internship$"))


def test_filter_by_source(page: Page, jobs_page):
    create_job(title="From LinkedIn", canonical_ids=["linkedin#1"])
    create_job(title="From StartupJobs", canonical_ids=["startupjobs#1"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='startupjobs']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("From StartupJobs")
    expect(page).to_have_url(re.compile(r"/jobs/\?source=startupjobs$"))


def test_filter_by_location(page: Page, jobs_page):
    create_job(title="Brno Developer", regions=["Brno"])
    create_job(title="Praha Developer", regions=["Praha"])
    create_job(title="Remote Developer", remote=True)
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='brno']").click()
    page.locator(".jobs-filters [data-jobs-tag='remote']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(2)
    expect(visible_jobs.filter(has_text="Brno Developer")).to_have_count(1)
    expect(visible_jobs.filter(has_text="Remote Developer")).to_have_count(1)
    expect(page).to_have_url(re.compile(r"/jobs/\?location=brno%7Cremote$"))


def test_only_tags_of_active_filters_are_highlighted(page: Page, jobs_page):
    create_job(
        title="Python Internship", tech_tags=["python"], employment_types=["internship"]
    )
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    job = page.locator(".jobs-item.tagged")
    expect(job.locator("[data-jobs-tag='python']")).to_have_class(
        re.compile(r"\bmatching\b")
    )
    expect(job.locator("[data-jobs-tag='internship']")).not_to_have_class(
        re.compile(r"\bmatching\b")
    )


def test_discord_jobs_are_not_filtered(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="Java Developer", tech_tags=["java"])
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)
    expect(page.locator(".jobs-item:not(.tagged)")).to_be_visible()
    expect(page.locator(".jobs-item:not(.tagged)")).to_contain_text("Discord Developer")


@pytest.mark.xfail(
    reason="Bug: matching compares tag slugs regardless of their type",
    strict=True,
    raises=AssertionError,
)
def test_tags_match_only_within_their_type(page: Page, jobs_page):
    create_job(title="Remote Developer", remote=True)
    create_job(title="Office Developer", tech_tags=["remote"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(
        ".jobs-filters [data-jobs-tag-type='location'][data-jobs-tag='remote']"
    ).click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Remote Developer")
