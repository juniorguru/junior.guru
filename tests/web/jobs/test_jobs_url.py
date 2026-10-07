import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_url_lists_types_and_tags_in_stable_order(page: Page, jobs_page):
    create_job(
        title="Python Internship", tech_tags=["python"], employment_types=["internship"]
    )
    create_job(
        title="Java Internship", tech_tags=["java"], employment_types=["internship"]
    )
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    page.locator(".jobs-filters [data-jobs-tag='internship']").click()
    page.locator(".jobs-filters [data-jobs-tag='java']").click()

    expect(page).to_have_url(
        re.compile(r"/jobs/\?employment=internship&technology=java%7Cpython$")
    )


def test_url_with_multiple_types_restores_filter(page: Page, jobs_page):
    create_job(
        title="Python Internship", tech_tags=["python"], employment_types=["internship"]
    )
    create_job(
        title="Java Internship", tech_tags=["java"], employment_types=["internship"]
    )
    create_job(
        title="Python Full-time", tech_tags=["python"], employment_types=["fulltime"]
    )
    jobs_page()
    page.goto("/jobs/?technology=java|python&employment=internship")

    active_tags = page.locator(".jobs-filters .jobs-tag.active")
    expect(active_tags).to_have_count(3)
    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(2)
    expect(visible_jobs.filter(has_text="Python Full-time")).to_have_count(0)


def test_url_with_unknown_tag_shows_all_jobs(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="Java Developer", tech_tags=["java"])
    jobs_page()
    page.goto("/jobs/?technology=cobol")

    expect(page.locator(".jobs-filters .jobs-tag.active")).to_have_count(0)
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)


@pytest.mark.xfail(
    reason="Bug: filtering removes all query parameters, not only the filter ones",
    strict=True,
    raises=AssertionError,
)
def test_unrelated_query_parameters_are_kept_on_load(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    jobs_page()
    page.goto("/jobs/?utm_source=newsletter")

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)
    expect(page).to_have_url(re.compile(r"/jobs/\?utm_source=newsletter$"))


@pytest.mark.xfail(
    reason="Bug: filtering removes all query parameters, not only the filter ones",
    strict=True,
    raises=AssertionError,
)
def test_unrelated_query_parameters_are_kept_on_filtering(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    jobs_page()
    page.goto("/jobs/?utm_source=newsletter")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    expect(page).to_have_url(re.compile(r"[?&]utm_source=newsletter(&|$)"))
    expect(page).to_have_url(re.compile(r"[?&]technology=python(&|$)"))
