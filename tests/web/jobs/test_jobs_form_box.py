from datetime import date

from playwright.sync_api import Page, expect
from web.helpers import create_job


def test_form_box_follows_second_regular_job(page: Page, jobs_page):
    for number in range(1, 4):
        create_job(title=f"Regular {number}", posted_on=date(2026, 1, 10 - number))
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.form + .jobs-item")).to_contain_text("Regular 3")


def test_form_box_is_present_without_jobs(page: Page, jobs_page):
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.form #github-profile-form")).to_be_visible()


def test_form_box_is_not_counted_as_job(page: Page, jobs_page):
    create_job(title="Python Developer", tech_tags=["python"])
    create_job(title="JavaScript Developer", tech_tags=["javascript"])
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    expect(page.locator(".jobs-item.tagged:visible")).to_have_count(1)


def test_form_box_moves_after_second_visible_regular_job(page: Page, jobs_page):
    for number in range(1, 5):
        tech_tags = ["javascript"] if number == 1 else ["python"]
        create_job(
            title=f"Regular {number}",
            posted_on=date(2026, 1, 10 - number),
            tech_tags=tech_tags,
        )
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    expect(page.locator(".jobs-item.form")).to_be_visible()
    expect(page.locator(".jobs-item.form + .jobs-item")).to_contain_text("Regular 4")
