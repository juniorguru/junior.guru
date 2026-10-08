import re

import pytest
from playwright.sync_api import Page, expect
from web.helpers import create_candidate


def test_url_lists_types_and_tags_in_stable_order(page: Page, candidates_page):
    """
    Types are in the order of the filters on the page, tags are sorted
    """
    create_candidate(name="Ada Lovelace", skills=["Python"], languages=["English"])
    create_candidate(name="Grace Hopper", skills=["COBOL"], languages=["English"])
    candidates_page()
    page.goto("/candidates/")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()
    page.locator(".candidates-filters [data-candidates-tag='english']").click()
    page.locator(".candidates-filters [data-candidates-tag='cobol']").click()

    expect(page).to_have_url(
        re.compile(r"/candidates/\?skill=cobol%7Cpython&language=english$")
    )


def test_url_with_multiple_types_restores_filter(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"], languages=["English"])
    create_candidate(name="Grace Hopper", skills=["COBOL"], languages=["English"])
    create_candidate(name="Linus Torvalds", skills=["Python"], languages=["Suomi"])
    candidates_page()
    page.goto("/candidates/?skill=cobol|python&language=english")

    active_tags = page.locator(".candidates-filters .candidates-tag.active")
    expect(active_tags).to_have_count(3)
    visible = page.locator(".candidates-item.tagged:visible")
    expect(visible).to_have_count(2)
    expect(visible.filter(has_text="Linus Torvalds")).to_have_count(0)


def test_url_with_unknown_tag_shows_all_candidates(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    page.goto("/candidates/?skill=fortran")

    expect(page.locator(".candidates-filters .candidates-tag.active")).to_have_count(0)
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(2)


def test_unrelated_query_parameters_are_kept_on_load(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    candidates_page()
    page.goto("/candidates/?utm_source=newsletter")

    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(1)
    expect(page).to_have_url(re.compile(r"/candidates/\?utm_source=newsletter$"))


@pytest.mark.xfail(
    reason="Bug: filtering removes all query parameters, not only the filter ones",
    strict=True,
    raises=AssertionError,
)
def test_unrelated_query_parameters_are_kept_on_filtering(page: Page, candidates_page):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    candidates_page()
    page.goto("/candidates/?utm_source=newsletter")

    page.locator(".candidates-filters [data-candidates-tag='python']").click()

    expect(page).to_have_url(re.compile(r"[?&]utm_source=newsletter(&|$)"))
    expect(page).to_have_url(re.compile(r"[?&]skill=python(&|$)"))


@pytest.mark.parametrize(
    "query, count",
    [
        ("skill=", 2),
        ("skill=Python", 2),
        ("skill=python|", 1),
        ("location=", 2),
        ("unknown=python", 2),
    ],
)
def test_url_with_odd_values_shows_candidates(
    page: Page, candidates_page, query: str, count: int
):
    create_candidate(name="Ada Lovelace", skills=["Python"])
    create_candidate(name="Grace Hopper", skills=["COBOL"])
    candidates_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(error))
    page.goto(f"/candidates/?{query}")

    expect(page.locator(".candidates-noscript")).to_have_count(0)
    expect(page.locator(".candidates-item.tagged:visible")).to_have_count(count)
    expect(page.locator(".candidates-empty")).to_be_hidden()
    assert errors == []
