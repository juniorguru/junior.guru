import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_discord_job, create_job


def test_discord_jobs_section_is_hidden_without_discord_jobs(page: Page, jobs_page):
    create_job(title="Python Developer")
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator("#club")).to_have_count(0)


@pytest.mark.parametrize(
    "count, text",
    [
        (1, "1 takový inzerát"),
        (3, "3 takové inzeráty"),
        (5, "5 takových inzerátů"),
    ],
)
def test_discord_jobs_section_counts_jobs(page: Page, jobs_page, count: int, text: str):
    create_job(title="Python Developer")
    for _ in range(count):
        create_discord_job()
    jobs_page()
    page.goto("/jobs/")

    expect(page.locator("#club")).to_be_visible()
    expect(page.locator("#club + p")).to_contain_text(text)
    expect(page.locator(".jobs-item:not(.tagged)")).to_have_count(count)


def test_clicking_discord_job_opens_discord(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Discord Developer")
    jobs_page()
    page.goto("/jobs/")

    job = page.locator(".jobs-item:not(.tagged)")
    requested_urls = []
    page.context.on("request", lambda request: requested_urls.append(request.url))
    with page.context.expect_page() as new_page_info:
        job.locator(".jobs-title-link").click()

    assert new_page_info.value.opener() == page
    assert "https://discord.com/channels/1/2/1" in requested_urls
    expect(job).not_to_have_class(re.compile(r"\bopen\b"))
    expect(page).to_have_url(re.compile(r"/jobs/$"))


def test_discord_job_shows_votes_and_comments_only_if_any(page: Page, jobs_page):
    create_job(title="Python Developer")
    create_discord_job(title="Popular", upvotes_count=7, comments_count=3)
    create_discord_job(title="Unnoticed", upvotes_count=0, comments_count=0)
    jobs_page()
    page.goto("/jobs/")

    popular = page.locator(".jobs-item:not(.tagged)", has_text="Popular")
    expect(popular.locator(".jobs-info-item")).to_have_count(3)
    expect(popular.locator(".jobs-info")).to_contain_text("7")
    expect(popular.locator(".jobs-info")).to_contain_text("3")
    unnoticed = page.locator(".jobs-item:not(.tagged)", has_text="Unnoticed")
    expect(unnoticed.locator(".jobs-info-item")).to_have_count(1)
