import re

from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_back_button_restores_previous_filter(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="Java Developer", tech_tags=["java"])
    create_job(title="Rust Developer", tech_tags=["rust"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    page.locator(".jobs-filters [data-jobs-tag='java']").click()
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)

    page.go_back()

    expect(page).to_have_url(re.compile(r"/jobs/\?technology=python$"))
    expect(page.locator(".jobs-filters .jobs-tag.active")).to_have_count(1)
    expect(page.locator(".jobs-filters [data-jobs-tag='python']")).to_have_class(
        re.compile(r"\bactive\b")
    )
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)


def test_back_button_restores_unfiltered_list(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="Java Developer", tech_tags=["java"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)

    page.go_back()

    expect(page).to_have_url(re.compile(r"/jobs/$"))
    expect(page.locator(".jobs-filters .jobs-tag.active")).to_have_count(0)
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(2)


def test_loading_page_adds_no_history_entry(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    jobs_page()
    page.add_init_script("window.initialHistoryLength = history.length")
    page.goto("/jobs/")
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)

    assert page.evaluate("history.length") == page.evaluate("initialHistoryLength")


def test_forward_button_works_after_going_back(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="Java Developer", tech_tags=["java"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()
    expect(page).to_have_url(re.compile(r"\?technology=python$"))
    page.go_back()
    expect(page).to_have_url(re.compile(r"/jobs/$"))
    page.go_forward()

    expect(page).to_have_url(re.compile(r"/jobs/\?technology=python$"))
    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)
