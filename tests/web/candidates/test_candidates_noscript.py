import re
from typing import Any

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_candidate


@pytest.fixture
def context_options() -> dict[str, Any]:
    return {"java_script_enabled": False}


def test_without_js_all_candidates_are_listed(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)
    expect(page.locator(".candidates-empty")).to_be_hidden()


def test_without_js_filters_show_error(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-filters")).to_have_class(
        re.compile(r"\bnoscript\b")
    )
    expect(page.locator(".candidates-noscript")).to_have_count(3)
    expect(page.locator(".candidates-noscript").first).to_be_visible()
    expect(
        page.locator(".candidates-filters [data-candidates-tag='python']")
    ).to_be_hidden()


def test_without_js_candidates_are_closed_links_to_github(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", github_username="ada", email="a@example.com")
    candidates_page()
    page.goto("/candidates/")

    item = page.locator(".candidates-item.tagged")
    expect(item.locator(".candidates-title-link")).to_be_visible()
    expect(item.locator(".candidates-title-link")).to_have_attribute(
        "href", "https://github.com/ada"
    )
    expect(item.locator(".candidates-actions")).to_be_hidden()
    expect(item.locator(".candidates-projects")).to_be_hidden()
    expect(item.locator(".candidates-action-email")).to_be_hidden()
