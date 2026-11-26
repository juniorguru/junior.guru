import re
from datetime import date

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_discord_job, create_job, create_submitted_job


def test_jobs_page_has_no_separate_discord_jobs_section(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job()
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator("#club")).to_have_count(0)


def test_discord_jobs_follow_highlighted_jobs(page: Page, jobs_page):
    for number in range(1, 6):
        create_job(title=f"Regular {number}", posted_on=date(2026, 1, 10 - number))
    create_submitted_job(title="Highlighted")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    titles = page.locator(".jobs-item .jobs-title-link").all_inner_texts()
    assert [title.strip() for title in titles] == [
        "Highlighted",
        "Discord Developer",
        "Regular 1",
        "Regular 2",
        "Regular 3",
        "Regular 4",
        "Regular 5",
    ]


def test_discord_jobs_are_highlighted(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.manual")).to_have_class(
        re.compile(r"\bhighlighted\b")
    )


def test_club_box_follows_fourth_regular_job(page: Page, jobs_page):
    for number in range(1, 6):
        create_job(title=f"Regular {number}", posted_on=date(2026, 1, 10 - number))
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.club + .jobs-item")).to_contain_text("Regular 5")


def test_club_box_is_present_without_discord_jobs(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    club_box = page.locator(".jobs-item.club")
    expect(club_box).to_be_visible()
    expect(club_box.locator(".club-teaser-button")).to_have_attribute(
        "href", re.compile(r"utm_source=jobs-box")
    )


def test_club_box_is_present_once_with_discord_jobs(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job()
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator(".jobs-item.club")).to_have_count(1)


@pytest.mark.parametrize(
    "count, text",
    [
        (1, "1 takový inzerát"),
        (3, "3 takové inzeráty"),
        (5, "5 takových inzerátů"),
    ],
)
def test_discord_job_counts_discord_jobs(page: Page, jobs_page, count: int, text: str):
    create_job(title="Python Developer")
    for _ in range(count):
        create_discord_job()
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.manual").first
    job.locator(".jobs-title-link").click()

    expect(page.locator(".jobs-item.manual")).to_have_count(count)
    expect(job.locator(".jobs-club-text")).to_contain_text(text)


def test_clicking_discord_job_opens_it(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.manual")
    job.locator(".jobs-title-link").click()

    expect(job).to_have_class(re.compile(r"\bopen\b"))
    expect(job.locator(".jobs-club")).to_be_visible()
    expect(page).to_have_url(re.compile(r"/jobs/$"))


def test_discord_job_is_closed_by_default(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.manual")
    expect(job.locator(".jobs-club")).to_be_hidden()


def test_discord_job_shows_votes_and_comments_only_if_any(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Popular", upvotes_count=7, comments_count=3)
    create_discord_job(title="Unnoticed", upvotes_count=0, comments_count=0)
    jobs_page()
    page.goto("/jobs/")

    popular = page.locator(".jobs-item.manual", has_text="Popular")
    expect(popular.locator(".jobs-info-item")).to_have_count(3)
    expect(popular.locator(".jobs-info")).to_contain_text("7")
    expect(popular.locator(".jobs-info")).to_contain_text("3")
    unnoticed = page.locator(".jobs-item.manual", has_text="Unnoticed")
    expect(unnoticed.locator(".jobs-info-item")).to_have_count(1)


def test_discord_jobs_are_shown_on_listing_pages(page: Page, jobs_page):
    create_job(title="Praha Developer", regions=["Praha"])
    create_discord_job(title="Discord Developer")
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    expect(page.locator(".jobs-item.manual")).to_contain_text("Discord Developer")


def test_discord_job_links_to_its_thread(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item.manual")
    job.locator(".jobs-title-link").click()

    expect(job.locator(".club-teaser-button")).to_have_attribute(
        "href", "https://discord.com/channels/1/2/1"
    )


def test_empty_listing_page_mentions_club_jobs(page: Page, jobs_page):
    create_job(title="Praha Developer", regions=["Praha"])
    create_discord_job(title="Discord Developer")
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    expect(page.locator(".jobs-empty-listing")).to_contain_text(
        "Zrovna tu nejsou žádné vhodné inzeráty, zbývají jen ty klubové."
    )


def test_empty_listing_page_without_club_jobs(page: Page, jobs_page):
    create_job(title="Praha Developer", regions=["Praha"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    empty = page.locator(".jobs-empty-listing")
    expect(empty).to_contain_text("Zrovna tu nejsou žádné vhodné inzeráty.")
    expect(empty).not_to_contain_text("klubové")


def test_club_box_follows_fourth_visible_regular_job_when_filtered(
    page: Page, jobs_page
):
    for number in range(1, 11):
        create_job(
            title=f"Regular {number}",
            posted_on=date(2026, 1, 20 - number),
            tech_tags=["python" if number % 2 else "java"],
        )
    jobs_page()
    page.goto("/jobs/")

    page.locator(".jobs-filters [data-jobs-tag='python']").click()

    items = page.locator(".jobs-item:visible").evaluate_all(
        """items => items.map(item => item.classList.contains("jobs-box")
            ? item.classList.contains("club") ? "club" : "form"
            : item.querySelector(".jobs-title-link").textContent.trim())"""
    )
    assert items == [
        *["Regular 1", "Regular 3", "form", "Regular 5", "Regular 7"],
        *["club", "Regular 9"],
    ]
