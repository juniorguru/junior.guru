import re

from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_parttime_page_shows_only_parttime_jobs(page: Page, jobs_page):
    create_job(title="Python Internship", employment_types=["internship"])
    create_job(title="Python Part-time", employment_types=["parttime"])
    create_job(title="Python Volunteering", employment_types=["volunteering"])
    create_job(title="Python Full-time", employment_types=["fulltime"])
    create_job(title="Python Untagged")
    jobs_page("/jobs/part-time/")
    page.goto("/jobs/part-time/")

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(3)
    expect(visible_jobs.filter(has_text="Full-time")).to_have_count(0)
    expect(visible_jobs.filter(has_text="Untagged")).to_have_count(0)
    expect(page).to_have_url(re.compile(r"/jobs/part-time/$"))


def test_parttime_page_offers_only_parttime_employment_types(page: Page, jobs_page):
    create_job(title="Internship", employment_types=["internship", "fulltime"])
    create_job(title="Full-time", employment_types=["fulltime", "contract"])
    jobs_page("/jobs/part-time/")
    page.goto("/jobs/part-time/")

    employment_tags = page.locator(
        ".jobs-filters [data-jobs-tag-type='employment']:visible"
    )
    expect(employment_tags).to_have_count(1)
    expect(employment_tags).to_have_attribute("data-jobs-tag", "internship")


def test_parttime_page_offers_all_locations(page: Page, jobs_page):
    create_job(
        title="Brno Internship", regions=["Brno"], employment_types=["internship"]
    )
    create_job(
        title="Praha Internship", regions=["Praha"], employment_types=["internship"]
    )
    jobs_page("/jobs/part-time/")
    page.goto("/jobs/part-time/")

    page.locator(".jobs-filters [data-jobs-tag='brno']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Brno Internship")
    expect(page).to_have_url(re.compile(r"/jobs/part-time/\?location=brno$"))
