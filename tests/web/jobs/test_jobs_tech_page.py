import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_job


@pytest.mark.parametrize(
    "url, tech_tags",
    [
        ("/jobs/python/", ["python"]),
        ("/jobs/tester/", ["testing"]),
        ("/jobs/javascript/", ["typescript"]),
        ("/jobs/ai/", ["buildingai"]),
    ],
)
def test_tech_page_shows_only_jobs_with_tech(
    page: Page, jobs_page, url: str, tech_tags: list[str]
):
    create_job(title="Matching Developer", tech_tags=tech_tags)
    create_job(title="Ruby Developer", tech_tags=["ruby"])
    jobs_page(url)
    page.goto(url)

    jobs = page.locator(".jobs-item.tagged")
    expect(jobs).to_have_count(1)
    expect(jobs).to_contain_text("Matching Developer")
    expect(page).to_have_url(re.compile(f"{url}$"))


def test_ai_page_ignores_generic_ai_tag(page: Page, jobs_page):
    create_job(title="AI Builder", tech_tags=["ai", "buildingai"])
    create_job(title="PHP Developer Using AI", tech_tags=["ai", "php"])
    jobs_page("/jobs/ai/")
    page.goto("/jobs/ai/")

    jobs = page.locator(".jobs-item.tagged")
    expect(jobs).to_have_count(1)
    expect(jobs).to_contain_text("AI Builder")


def test_tech_tag_cannot_be_turned_off(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    jobs_page("/jobs/python/")
    page.goto("/jobs/python/")

    tech_tag = page.locator(".jobs-filters [data-jobs-tag='python']")
    tech_tag.click(force=True)

    expect(tech_tag).to_have_class(re.compile(r"\bactive\b"))
    expect(page).to_have_url(re.compile(r"/jobs/python/$"))


def test_tech_page_offers_only_its_tech(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python", "django"])
    jobs_page("/jobs/python/")
    page.goto("/jobs/python/")

    tech_tags = page.locator(".jobs-filters [data-jobs-tag-type='technology']")
    expect(tech_tags).to_have_count(1)


def test_tech_page_with_other_filters(page: Page, jobs_page):
    create_job(title="Brno Python", regions=["Brno"], tech_tags=["python"])
    create_job(title="Praha Python", regions=["Praha"], tech_tags=["python"])
    jobs_page("/jobs/python/")
    page.goto("/jobs/python/")

    page.locator(".jobs-filters [data-jobs-tag='brno']").click()

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Brno Python")
    expect(page).to_have_url(re.compile(r"/jobs/python/\?location=brno$"))


def test_tech_page_url_restores_filter(page: Page, jobs_page):
    create_job(title="Brno Python", regions=["Brno"], tech_tags=["python"])
    create_job(title="Praha Python", regions=["Praha"], tech_tags=["python"])
    jobs_page("/jobs/python/")
    page.goto("/jobs/python/?location=praha")

    visible_jobs = page.locator(".jobs-item.tagged:visible")
    expect(visible_jobs).to_have_count(1)
    expect(visible_jobs).to_contain_text("Praha Python")


def test_tech_page_empty_state_links_other_jobs(page: Page, jobs_page):
    create_job(title="Ruby Developer", tech_tags=["ruby"])
    jobs_page("/jobs/java/")
    page.goto("/jobs/java/")

    empty = page.locator(".jobs-empty-listing")
    expect(empty).to_be_visible()
    expect(empty.locator("a")).to_have_text("ostatní nabídky")
    expect(page.locator(".jobs-empty")).to_be_hidden()


def test_tech_page_empty_state_with_filters(page: Page, jobs_page):
    create_job(title="Ruby Developer", tech_tags=["ruby"])
    jobs_page("/jobs/java/")
    page.goto("/jobs/java/")

    page.locator(".jobs-filters [data-jobs-tag='brno']").click()

    expect(page.locator(".jobs-empty-listing")).to_be_visible()
    expect(page.locator(".jobs-empty")).to_be_hidden()


def test_tech_page_empty_by_filters_suggests_remote_tag(page: Page, jobs_page):
    create_job(title="Praha Python", regions=["Praha"], tech_tags=["python"])
    jobs_page("/jobs/python/")
    page.goto("/jobs/python/")

    page.locator(".jobs-filters [data-jobs-tag='brno']").click()

    empty = page.locator(".jobs-empty")
    expect(empty).to_be_visible()
    expect(empty).to_contain_text("#remote")
    expect(page.locator(".jobs-empty-listing")).to_be_hidden()
