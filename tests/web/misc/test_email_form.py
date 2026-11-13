import re
from collections.abc import Callable

import pytest
from playwright.sync_api import Page, expect
from web.conftest import render


@pytest.fixture
def news_page(serve: Callable[[str], None]) -> None:
    context = {"newsletter_subscribers_count": 42, "newsletter_issues": []}
    serve(render("news.jinja", context, "/news/"))


@pytest.mark.parametrize(
    "url, visible_id",
    [
        ("/news/", "email-form"),
        ("/news/?email_address=ada@example.com", "email-subscribed"),
        ("/news/?email_address=confirmed", "email-confirmed"),
    ],
)
def test_shows_state_from_url(page: Page, news_page, url: str, visible_id: str):
    page.goto(url)

    expect(page.locator(".newsletter-container:visible")).to_have_attribute(
        "id", visible_id
    )


def test_reset_shows_form(page: Page, news_page):
    page.goto("/news/?email_address=confirmed")
    page.locator("#email-reset").click()

    expect(page.locator(".newsletter-container:visible")).to_have_attribute(
        "id", "email-form"
    )


def test_reset_keeps_hash(page: Page, news_page):
    page.goto("/news/?email_address=confirmed#archive")
    page.locator("#email-reset").click()

    expect(page).to_have_url(re.compile(r"/news/#archive$"))


def test_back_button_restores_state(page: Page, news_page):
    page.goto("/news/?email_address=confirmed")
    page.locator("#email-reset").click()
    expect(page.locator("#email-form")).to_be_visible()

    page.go_back()

    expect(page.locator(".newsletter-container:visible")).to_have_attribute(
        "id", "email-confirmed"
    )
