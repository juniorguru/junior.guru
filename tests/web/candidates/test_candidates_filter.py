import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_candidate

from jg.coop.lib.location import REGIONS


def test_shows_all_candidates_without_filter(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-item.tagged")).to_have_count(2)
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)
    expect(page.locator(".candidates-empty")).to_be_hidden()
    expect(page).to_have_url(re.compile(r"/candidates/$"))


def test_filter_tags_are_revealed_in_all_groups(page: Page, candidates_page):
    """
    The filters got wrapped in another element, which shares the class
    with the first group of tags, so the JS must look for the right one
    """
    create_candidate(
        name="Ada Lovelace", regions=["Brno"], skills=["Python"], languages=["English"]
    )
    candidates_page()
    page.goto("/candidates/")

    filters = page.locator(".candidates-filters")
    expect(filters.locator("[data-candidates-tag='brno']")).to_be_visible()
    expect(filters.locator("[data-candidates-tag='python']")).to_be_visible()
    expect(filters.locator("[data-candidates-tag='english']")).to_be_visible()
    expect(filters.locator(".candidates-tag:not(:visible)")).to_have_count(0)
    expect(page.locator(".candidates-noscript")).to_have_count(0)
    expect(filters).not_to_have_class(re.compile(r"\bnoscript\b"))


def test_location_filter_offers_anywhere_and_all_regions(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", regions=["Brno"])
    candidates_page()
    page.goto("/candidates/")

    location_tags = page.locator(
        ".candidates-filters [data-candidates-tag-type='location']"
    )
    expect(location_tags.first).to_have_text("#kdekoliv")
    expect(location_tags).to_have_count(len(REGIONS) + 1)


def test_skill_and_language_filters_offer_only_existing_tags(
    page: Page, candidates_page
):
    create_candidate(name="Ada Lovelace", skills=["Python"], languages=["English"])
    create_candidate(name="Grace Hopper", skills=["COBOL"], languages=["English"])
    candidates_page()
    page.goto("/candidates/")

    filters = page.locator(".candidates-filters")
    expect(filters.locator("[data-candidates-tag-type='skill']")).to_have_text(
        ["#cobol", "#python"]
    )
    expect(filters.locator("[data-candidates-tag-type='language']")).to_have_text(
        ["#english"]
    )


def test_clicking_tag_filters_candidates(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()

    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(1)
    expect(visible).to_contain_text("Ada Lovelace")
    expect(visible.locator("[data-candidates-tag='python']")).to_have_class(
        re.compile(r"\bmatching\b")
    )
    expect(page).to_have_url(re.compile(r"/candidates/\?skill=python$"))


def test_clicking_tag_again_resets_filter(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    tag = page.locator(".candidates-filters [data-candidates-tag='python']")
    tag.click()
    tag.click()

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)
    expect(page.locator(".candidates-item .candidates-tag.matching")).to_have_count(0)
    expect(page).to_have_url(re.compile(r"/candidates/$"))


def test_url_restores_filter(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/?skill=cobol")

    expect(
        page.locator(".candidates-filters [data-candidates-tag='cobol']")
    ).to_have_class(re.compile(r"\bactive\b"))
    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(1)
    expect(visible).to_contain_text("Grace Hopper")


def test_tags_of_same_type_are_alternatives(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    create_candidate(name="Linus Torvalds", skills=["C"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    page.locator(".candidates-filters [data-candidates-tag='cobol']").click()

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)
    expect(page).to_have_url(re.compile(r"\?skill=cobol%7Cpython$"))


def test_tags_of_different_types_must_all_match(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"], languages=["English"])
    create_candidate(name="Grace Hopper", skills=["Python"], languages=["Deutsch"])
    create_candidate(name="Linus Torvalds", skills=["C"], languages=["English"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    page.locator(".candidates-filters [data-candidates-tag='english']").click()

    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(1)
    expect(visible).to_contain_text("Ada Lovelace")


def test_filter_by_location(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", regions=["Brno"])
    create_candidate(name="Grace Hopper", regions=["Praha"])
    create_candidate(name="Linus Torvalds")
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='brno']").click()
    page.locator(".candidates-filters [data-candidates-tag='kdekoliv']").click()

    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(2)
    expect(visible.filter(has_text="Ada Lovelace")).to_have_count(1)
    expect(visible.filter(has_text="Linus Torvalds")).to_have_count(1)
    expect(page).to_have_url(re.compile(r"/candidates/\?location=brno%7Ckdekoliv$"))


def test_filter_by_language(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", languages=["English"])
    create_candidate(name="Grace Hopper", languages=["Deutsch"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='deutsch']").click()

    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(1)
    expect(visible).to_contain_text("Grace Hopper")
    expect(page).to_have_url(re.compile(r"/candidates/\?language=deutsch$"))


def test_only_tags_of_active_filters_are_highlighted(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"], languages=["English"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()

    candidate = page.locator(".candidates-item.tagged")
    expect(candidate.locator("[data-candidates-tag='python']")).to_have_class(
        re.compile(r"\bmatching\b")
    )
    expect(candidate.locator("[data-candidates-tag='english']")).not_to_have_class(
        re.compile(r"\bmatching\b")
    )


def test_no_matching_candidates_shows_empty_state(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", regions=["Brno"], skills=["Python"])
    create_candidate(name="Grace Hopper", regions=["Praha"], skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    page.locator(".candidates-filters [data-candidates-tag='praha']").click()

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(0)
    empty = page.locator(".candidates-empty")
    expect(empty).to_be_visible()
    expect(empty).to_contain_text("#kdekoliv")


def test_tags_outside_filters_are_ignored(page: Page, candidates_page):
    """
    The #kdekoliv tag in the empty state note has the 'active' class too,
    so it must not be mistaken for an active filter
    """
    create_candidate(name="Ada Lovelace", regions=["Brno"], skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    expect(page.locator(".candidates-empty .candidates-tag.active")).to_have_count(1)
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)
    expect(page).to_have_url(re.compile(r"/candidates/$"))

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    page.locator(".candidates-filters [data-candidates-tag='kdekoliv']").click()
    page.locator(".candidates-filters [data-candidates-tag='kdekoliv']").click()

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)
    expect(page).to_have_url(re.compile(r"/candidates/\?skill=python$"))


def test_tags_of_candidates_are_not_filters(page: Page, candidates_page):
    """
    Tags of candidates and tags in filters share the same wrapper class,
    so the filters must be selected by their own container
    """
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    tag = page.locator(".candidates-item.tagged [data-candidates-tag='python']")
    tag.dispatch_event("click")

    expect(tag).not_to_have_class(re.compile(r"\bactive\b"))
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)
    expect(page).to_have_url(re.compile(r"/candidates/$"))


@pytest.mark.xfail(
    reason="Bug: filter tags are spans, so they can't be focused or used by keyboard",
    strict=True,
    raises=AssertionError,
)
def test_tags_can_be_used_by_keyboard(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/")

    tag = page.locator(".candidates-filters [data-candidates-tag='python']")
    for _ in range(page.locator("a, button, [tabindex]").count() + 1):
        page.keyboard.press("Tab")
        if tag.evaluate("tag => tag === document.activeElement"):
            break
    expect(tag).to_be_focused()
    page.keyboard.press("Enter")

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)


@pytest.mark.xfail(
    reason="Bug: matching compares tag slugs regardless of their type",
    strict=True,
    raises=AssertionError,
)
def test_tags_match_only_within_their_type(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", regions=["Brno"])
    create_candidate(name="Grace Hopper", regions=["Praha"], skills=["Brno"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(
        ".candidates-filters "
        "[data-candidates-tag-type='location'][data-candidates-tag='brno']"
    ).click()

    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(1)
    expect(visible).to_contain_text("Ada Lovelace")
