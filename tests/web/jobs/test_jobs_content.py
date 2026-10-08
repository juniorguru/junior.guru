import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect
from web.helpers import (
    create_discord_job,
    create_job,
    create_submitted_job,
    hide_subscribe_box,
)


IMAGES_DIR = Path("src/jg/coop/images")


@pytest.mark.parametrize(
    "url, heading",
    [
        ("/jobs/", "Práce v IT pro juniory"),
        ("/jobs/remote/", "Práce na dálku pro juniory"),
        ("/jobs/brno/", "Práce pro juniory: Brno"),
        ("/jobs/hradec-kralove/", "Práce pro juniory: Hradec Králové"),
    ],
)
def test_heading(page: Page, jobs_page, url: str, heading: str):
    create_job(title="Python Developer")
    jobs_page(url)
    page.goto(url)

    expect(page.locator("h1")).to_have_text(heading)


def test_intro_is_a_paragraph(page: Page, jobs_page):
    """
    Regression: an indented line in the intro used to render as a code block
    """
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    lead = page.locator(".lead")
    expect(lead.locator("pre, code")).to_have_count(0)
    expect(lead.locator("p").first).to_contain_text(
        "Nabídky práce v programování, testování a datové analytice."
    )


def test_region_page_intro_is_shorter(page: Page, jobs_page):
    create_job(title="Brno Developer", regions=["Brno"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")

    lead = page.locator(".lead")
    expect(lead).not_to_contain_text("Nabídky práce v programování")
    expect(lead.locator("pre, code")).to_have_count(0)
    expect(lead.locator("p").first).to_contain_text("Už žádné")


def test_link_to_all_regions_only_on_region_page(page: Page, jobs_page):
    create_job(title="Brno Developer", regions=["Brno"])
    jobs_page("/jobs/brno/")
    page.goto("/jobs/brno/")
    expect(page.locator(".jobs-filters .jobs-tag-link")).to_be_visible()

    jobs_page()
    page.goto("/jobs/")
    expect(page.locator(".jobs-filters .jobs-tag-link")).to_have_count(0)


def test_location_is_shown_only_if_known(page: Page, jobs_page):
    """
    Regression: jobs without location used to show a question mark
    """
    create_job(title="Brno Developer", regions=["Brno"])
    create_job(title="Nowhere Developer")
    jobs_page()
    page.goto("/jobs/")

    brno = page.locator(".jobs-item", has_text="Brno Developer")
    expect(brno.locator(".jobs-info-item")).to_have_count(2)
    expect(brno.locator(".jobs-info")).to_contain_text("Brno")
    nowhere = page.locator(".jobs-item", has_text="Nowhere Developer")
    expect(nowhere.locator(".jobs-info-item")).to_have_count(1)
    expect(nowhere.locator(".jobs-info")).not_to_contain_text("?")


def test_company_website_link_only_if_known(page: Page, jobs_page):
    create_job(title="With Website", company_url="https://example.com/company")
    create_job(title="Without Website")
    jobs_page()
    page.goto("/jobs/")

    with_website = page.locator(".jobs-item", has_text="With Website")
    expect(with_website.locator(".jobs-company-link")).to_have_count(5)
    expect(with_website.locator(".jobs-company-link").last).to_have_attribute(
        "href", "https://example.com/company"
    )
    without_website = page.locator(".jobs-item", has_text="Without Website")
    expect(without_website.locator(".jobs-company-link")).to_have_count(4)


def test_submitted_job_is_highlighted_and_links_to_junior_guru(page: Page, jobs_page):
    create_job(title="Scraped Developer")
    create_submitted_job("abc123", title="Submitted Developer")
    jobs_page()
    page.goto("/jobs/")

    hide_subscribe_box(page)
    jobs = page.locator(".jobs-item.tagged")
    submitted = jobs.first
    expect(submitted).to_contain_text("Submitted Developer")
    expect(submitted).to_have_class(re.compile(r"\bhighlighted\b"))
    expect(jobs.last).not_to_have_class(re.compile(r"\bhighlighted\b"))

    submitted.locator(".jobs-title-link").click()
    continue_link = submitted.locator(".jobs-action-button.continue")
    expect(continue_link).to_have_attribute("href", "/jobs/abc123/")
    expect(continue_link).not_to_have_attribute("target", "_blank")
    continue_link.click()

    expect(page).to_have_url("https://junior.guru/jobs/abc123/")
    assert len(page.context.pages) == 1


@pytest.mark.parametrize(
    "upvotes_count, comments_count, counts",
    [
        (4, 0, ["4"]),
        (0, 2, ["2"]),
        (4, 2, ["4", "2"]),
        (0, 0, []),
    ],
)
def test_discussion_button_only_if_job_is_in_club(
    page: Page,
    jobs_page,
    upvotes_count: int,
    comments_count: int,
    counts: list[str],
):
    create_job(
        title="Discussed Developer",
        discord_url="https://discord.com/channels/1/2/3",
        upvotes_count=upvotes_count,
        comments_count=comments_count,
    )
    create_job(title="Quiet Developer")
    jobs_page()
    page.goto("/jobs/")

    discussed = page.locator(".jobs-item", has_text="Discussed Developer")
    club = discussed.locator(".jobs-action-club")
    expect(club.locator(".jobs-action-button.club")).to_have_attribute(
        "href", "https://discord.com/channels/1/2/3"
    )
    expect(club.locator("span")).to_have_text(counts)
    quiet = page.locator(".jobs-item", has_text="Quiet Developer")
    expect(quiet.locator(".jobs-action-club")).to_have_count(0)
    expect(quiet.locator(".jobs-action-button.continue")).to_have_count(1)


def test_logos_exist(page: Page, jobs_page):
    """
    Regression: Discord jobs used to point to a logo which didn't exist
    """
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    urls = page.locator(".jobs-image").evaluate_all(
        "images => images.map(image => image.src)"
    )
    assert len(urls) == 2
    for url in urls:
        path = IMAGES_DIR / url.removeprefix("https://junior.guru/static/")
        assert path.is_file(), f"{url} doesn't exist"
