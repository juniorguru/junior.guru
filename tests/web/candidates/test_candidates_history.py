import re

from playwright.sync_api import Page, expect
from web.helpers import create_candidate


def test_back_button_restores_previous_filter(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    create_candidate(name="Linus Torvalds", skills=["C"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    page.locator(".candidates-filters [data-candidates-tag='cobol']").click()
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)

    page.go_back()

    expect(page).to_have_url(re.compile(r"/candidates/\?skill=python$"))
    expect(page.locator(".candidates-filters .candidates-tag.active")).to_have_count(1)
    expect(
        page.locator(".candidates-filters [data-candidates-tag='python']")
    ).to_have_class(re.compile(r"\bactive\b"))
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)


def test_back_button_restores_unfiltered_list(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)

    page.go_back()

    expect(page).to_have_url(re.compile(r"/candidates/$"))
    expect(page.locator(".candidates-filters .candidates-tag.active")).to_have_count(0)
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)


def test_loading_page_adds_no_history_entry(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    candidates_page()
    page.add_init_script("window.initialHistoryLength = history.length")
    page.goto("/candidates/")
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)

    assert page.evaluate("history.length") == page.evaluate("initialHistoryLength")


def test_forward_button_works_after_going_back(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    expect(page).to_have_url(re.compile(r"\?skill=python$"))
    page.go_back()
    expect(page).to_have_url(re.compile(r"/candidates/$"))
    page.go_forward()

    expect(page).to_have_url(re.compile(r"/candidates/\?skill=python$"))
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)
