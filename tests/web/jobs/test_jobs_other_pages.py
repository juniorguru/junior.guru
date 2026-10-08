"""
The JS bundle is shared by all pages, so the jobs JS must not break other pages
"""

from collections.abc import Callable

from playwright.sync_api import Page, expect
from web.conftest import wrap_html


HTML = """
<h1>Some page</h1>
<p><a href="#section">Jump to section</a></p>
<h2 id="section">Section</h2>
"""


def test_page_without_jobs_has_no_errors(page: Page, serve: Callable[[str], None]):
    serve(wrap_html(HTML))
    errors = []
    page.on("pageerror", lambda error: errors.append(error))
    page.goto("/some-page/")

    expect(page.locator("h1")).to_have_text("Some page")
    page.wait_for_load_state("load")
    assert errors == []


def test_page_without_jobs_has_no_errors_on_anchor_links(
    page: Page, serve: Callable[[str], None]
):
    serve(wrap_html(HTML))
    errors = []
    page.on("pageerror", lambda error: errors.append(error))
    page.goto("/some-page/")

    page.get_by_text("Jump to section").click()
    expect(page).to_have_url("https://junior.guru/some-page/#section")
    assert errors == []

    page.go_back()
    expect(page).to_have_url("https://junior.guru/some-page/")

    assert errors == []
