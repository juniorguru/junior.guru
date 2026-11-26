from collections.abc import Callable
from urllib.parse import parse_qs, urlparse

import pytest
from playwright.sync_api import Page, expect
from web.conftest import render_string


def serve_form(serve: Callable[[str], None], args: str = "") -> None:
    source = (
        "{% from 'macros.html' import github_profile_form with context %}"
        f"{{{{ github_profile_form({args}) }}}}"
    )
    serve(render_string(source, {}, "/"))


@pytest.fixture
def github_profile_page(page: Page, serve: Callable[[str], None]) -> None:
    serve_form(serve)
    page.add_init_script("window.open = (...args) => { window.opened = args; };")


def submit(page: Page, value: str) -> None:
    page.goto("/")
    page.locator("#github-profile-input").fill(value)
    page.locator("#github-profile-form [type=submit]").click()


def test_opens_issue_with_username(page: Page, github_profile_page):
    submit(page, "https://github.com/honzajavorek/")
    url = urlparse(page.evaluate("window.opened[0]"))

    assert parse_qs(url.query) == {
        "template": ["check.md"],
        "title": ["Zpětná vazba na profil @honzajavorek"],
        "body": [
            ("Kuřátko, mrkni prosím na @honzajavorek, díky!\n\n<!-- src: handbook -->")
        ],
    }


def test_opens_issue_in_new_tab(page: Page, github_profile_page):
    submit(page, "honzajavorek")

    assert page.evaluate("window.opened.slice(1)") == ["_blank", "noopener"]


def test_shows_normalized_username(page: Page, github_profile_page):
    submit(page, "https://github.com/honzajavorek/")

    expect(page.locator("#github-profile-input")).to_have_value("@honzajavorek")


def test_submitting_twice_doesnt_accumulate_username(page: Page, github_profile_page):
    submit(page, "honzajavorek")
    page.locator("#github-profile-form [type=submit]").click()
    url = urlparse(page.evaluate("window.opened[0]"))

    assert parse_qs(url.query)["title"] == ["Zpětná vazba na profil @honzajavorek"]


def test_homepage_form_marks_placement(page: Page, serve: Callable[[str], None]):
    serve_form(serve, "homepage=True")
    page.add_init_script("window.open = (...args) => { window.opened = args; };")
    submit(page, "honzajavorek")
    url = urlparse(page.evaluate("window.opened[0]"))

    assert parse_qs(url.query)["body"][0].endswith("<!-- src: homepage -->")
