from collections.abc import Callable

import pytest
from playwright.sync_api import Page, expect
from web.conftest import render_string


DISCORD_URL = "https://discord.com/channels/769966886598737931/123"


@pytest.fixture
def discord_page(serve: Callable[[str], None]) -> None:
    source = (
        "{% from 'macros.html' import discord_dialog with context %}"
        f'<p><a class="discord-link" href="{DISCORD_URL}" target="_blank">Discord</a></p>'
        "{{ discord_dialog() }}"
    )
    serve(render_string(source, {}, "/"))


def test_link_opens_dialog(page: Page, discord_page):
    page.goto("/")
    page.locator(".discord-link").click()

    expect(page.locator(".discord-dialog")).to_be_visible()


def test_dialog_continues_to_link(page: Page, discord_page):
    page.goto("/")
    page.locator(".discord-link").click()

    expect(page.locator(".discord-dialog-continue")).to_have_attribute(
        "href", DISCORD_URL
    )


def test_click_inside_dialog_keeps_it_open(page: Page, discord_page):
    page.goto("/")
    page.locator(".discord-link").click()
    page.locator(".discord-dialog p").click()

    expect(page.locator(".discord-dialog")).to_be_visible()


def test_click_on_dialog_padding_keeps_it_open(page: Page, discord_page):
    page.goto("/")
    page.locator(".discord-link").click()
    page.locator(".discord-dialog").click(position={"x": 2, "y": 2})

    expect(page.locator(".discord-dialog")).to_be_visible()


def test_click_on_backdrop_closes_dialog(page: Page, discord_page):
    page.goto("/")
    page.locator(".discord-link").click()
    page.mouse.click(2, 2)

    expect(page.locator(".discord-dialog")).to_be_hidden()


@pytest.mark.parametrize(
    "macro_args, expected",
    [
        (
            "'handbook-channels'",
            "/club/?utm_source=handbook-channels&utm_medium=web&utm_campaign=jaro",
        ),
        (
            "'handbook-channels', 'cv'",
            (
                "/club/?utm_source=handbook-channels&utm_medium=web&utm_campaign=jaro"
                "&utm_content=cv"
            ),
        ),
    ],
)
def test_utm_macro_passes_params_to_club_link(
    page: Page, serve: Callable[[str], None], macro_args: str, expected: str
):
    source = (
        "{% from 'macros.html' import discord_dialog, discord_dialog_utm with context %}"
        f'<p><a class="discord-link" href="{DISCORD_URL}" target="_blank"'
        f" {{{{ discord_dialog_utm({macro_args}) }}}}>Discord</a></p>"
        "{{ discord_dialog() }}"
    )
    serve(render_string(source, {}, "/"))
    page.goto("/")
    page.locator(".discord-link").click()

    expect(page.locator(".discord-dialog-club")).to_have_attribute(
        "href", f"https://junior.guru{expected}"
    )
