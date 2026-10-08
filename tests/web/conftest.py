"""
Harness for testing the behavior of interactive pages in a real browser

Each test fills an in-memory database with sample data, renders a single
Jinja page from src/jg/coop/web/docs with the real template filters and
macros, wraps it in a minimal HTML document with the real JS and CSS bundle,
and serves it to Playwright as if it was https://junior.guru/<path>.
"""

import subprocess
from collections.abc import Callable, Generator
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from jinja2 import Environment, FileSystemLoader
from mkdocs.utils.meta import get_data as parse_document
from mkdocs.utils.templates import url_filter
from peewee import SqliteDatabase
from playwright.sync_api import Browser, Page, Route, expect, sync_playwright

from jg.coop.lib import template_filters
from jg.coop.lib.mkdocs_jinja import get_filters
from jg.coop.web.context import get_jobs_context
from jg.coop.web.generators import generate_region_jobs_pages

from testing_utils import prepare_test_db


WEB_DIR = Path("src/jg/coop/web")

DOCS_DIR = WEB_DIR / "docs"

MACROS_DIR = WEB_DIR / "macros"

BASE_URL = "https://junior.guru"


# Pages are served from memory, so there's no need to wait long
expect.set_options(timeout=2_000)


@pytest.fixture
def test_db() -> Generator[SqliteDatabase]:
    yield from prepare_test_db()


@pytest.fixture(scope="session")
def static_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    static_dir = tmp_path_factory.mktemp("static")
    subprocess.run(["node", "esbuild.js", str(static_dir.absolute())], check=True)
    return static_dir


def render(
    template_path: str,
    context: dict[str, Any],
    url: str,
    page_meta: dict[str, Any] | None = None,
) -> str:
    env = Environment(loader=FileSystemLoader(MACROS_DIR))
    env.filters.update(get_filters())
    env.filters["url"] = url_filter
    env.filters["md"] = template_filters.md
    env.filters["docs_url"] = lambda files, src_path: "#"

    source = (DOCS_DIR / template_path).read_text(encoding="utf-8-sig")
    content, meta = parse_document(source)
    page = SimpleNamespace(url=url.lstrip("/"), meta=meta | (page_meta or {}))
    html = env.from_string(content).render(page=page, pages=[], base_url="/", **context)
    return wrap_html(html)


def wrap_html(html: str) -> str:
    """
    Wraps given HTML in a minimal document with the real JS and CSS bundle
    """
    return (
        "<!DOCTYPE html>"
        '<html lang="cs"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link rel="stylesheet" href="/static/css/index.css">'
        '<script defer src="/static/js/index.js"></script>'
        f"</head><body>{html}</body></html>"
    )


# Module scope, because the sync Playwright API keeps an event loop running,
# which would break any async tests executed while the browser is open
@pytest.fixture(scope="module")
def browser() -> Generator[Browser]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def context_options() -> dict[str, Any]:
    """
    Options for the browser context, override to change them for a module or test
    """
    return {}


@pytest.fixture
def page(
    browser: Browser, static_dir: Path, context_options: dict[str, Any]
) -> Generator[Page]:
    context = browser.new_context(base_url=BASE_URL, **context_options)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def serve(page: Page, static_dir: Path) -> Callable[[str], None]:
    """
    Serves given HTML for any page URL, and the JS/CSS bundle for /static/

    Requests outside of junior.guru are blocked, so that clicking an external
    link never reaches the internet, even if it opens in a new tab.
    """

    def serve(html: str) -> None:
        def handle(route: Route) -> None:
            if not route.request.url.startswith(f"{BASE_URL}/"):
                route.abort()
                return
            path = route.request.url.removeprefix(BASE_URL).split("?")[0]
            if path.startswith("/static/"):
                file_path = static_dir / path.removeprefix("/static/")
                if file_path.is_file():
                    route.fulfill(path=file_path)
                else:
                    route.fulfill(status=404)
            else:
                route.fulfill(body=html, content_type="text/html; charset=utf-8")

        page.context.route("**/*", handle)

    return serve


@pytest.fixture
def jobs_page(test_db: SqliteDatabase, serve: Callable[[str], None]) -> Callable:
    """
    Renders jobs.jinja from whatever jobs are in the test database

    For region pages, such as /jobs/brno/, it takes page metadata
    from the same generator which creates those pages for the real website.
    """

    def jobs_page(url: str = "/jobs/") -> None:
        page_meta = None
        if url != "/jobs/":
            page_meta = get_region_jobs_page_meta(url)
        serve(render("jobs.jinja", get_jobs_context(), url, page_meta))

    return jobs_page


def get_region_jobs_page_meta(url: str) -> dict[str, Any]:
    path = url.strip("/") + ".jinja"
    for document in generate_region_jobs_pages():
        if document.path == path:
            return document.meta
    raise ValueError(f"No region jobs page for {url}")
