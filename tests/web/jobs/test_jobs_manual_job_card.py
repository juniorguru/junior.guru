from collections.abc import Callable
from types import SimpleNamespace

import pytest
from playwright.sync_api import Page, expect
from web.conftest import render_string


DISCORD_URL = "https://discord.com/channels/769966886598737931/123/456"


@pytest.fixture
def manual_job_page(serve: Callable[[str], None]) -> None:
    """
    Renders a manual job card on a page with the Discord dialog, as the real website does
    """
    source = (
        "{% from 'macros.html' import discord_dialog, manual_job_card with context %}"
        '<ul class="jobs-list">{{ manual_job_card(job, 1) }}</ul>'
        "{{ discord_dialog() }}"
    )
    job = SimpleNamespace(
        title="Discord Developer",
        url=DISCORD_URL,
        author=SimpleNamespace(initials="K.Ž."),
        upvotes_count=0,
        comments_count=0,
    )
    members = [SimpleNamespace(avatar_path="avatars-members/1.webp")]
    context = {"job": job, "members": members, "members_total_count": 1}
    serve(render_string(source, context, "/jobs/"))


def test_clicking_title_opens_job_without_dialog(page: Page, manual_job_page):
    page.goto("/jobs/")
    page.locator(".jobs-title-link").click()

    expect(page.locator(".jobs-club")).to_be_visible()
    expect(page.locator(".discord-dialog")).to_be_hidden()


def test_button_leads_to_job_thread_through_dialog(page: Page, manual_job_page):
    page.goto("/jobs/")
    page.locator(".jobs-title-link").click()
    page.locator(".club-teaser-button").click()

    expect(page.locator(".discord-dialog")).to_be_visible()
    expect(page.locator(".discord-dialog-continue")).to_have_attribute(
        "href", DISCORD_URL
    )


def test_avatars_load_lazily(page: Page, manual_job_page):
    page.goto("/jobs/")

    expect(page.locator(".members img")).to_have_attribute("loading", "lazy")
