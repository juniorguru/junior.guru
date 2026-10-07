"""
Harness for testing the behavior of interactive pages in a real browser

Each test fills an in-memory database with sample data, renders a single
Jinja page from src/jg/coop/web/docs with the real template filters and
macros, wraps it in a minimal HTML document with the real JS and CSS bundle,
and serves it to Playwright as if it was https://junior.guru/<path>.
"""

import subprocess
from collections.abc import Callable, Generator
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from jinja2 import Environment, FileSystemLoader
from mkdocs.utils.meta import get_data as parse_document
from mkdocs.utils.templates import url_filter
from peewee import SqliteDatabase
from playwright.sync_api import Browser, Page, Route, sync_playwright

from jg.coop.lib import template_filters
from jg.coop.lib.mkdocs_jinja import get_filters
from jg.coop.models.job import ListedJob
from jg.coop.web.context import get_jobs_context

from testing_utils import prepare_test_db


WEB_DIR = Path("src/jg/coop/web")

DOCS_DIR = WEB_DIR / "docs"

MACROS_DIR = WEB_DIR / "macros"

BASE_URL = "https://junior.guru"


@pytest.fixture
def test_db() -> Generator[SqliteDatabase]:
    yield from prepare_test_db()


def create_job(**kwargs) -> ListedJob:
    title = kwargs.pop("title", "Junior Developer")
    return ListedJob.create(
        **{
            "title": title,
            "posted_on": date(2026, 1, 1),
            "lang": "cs",
            "description_html": f"<p>{title}</p>",
            "description_text": title,
            "description_discord": title,
            "url": f"https://example.com/jobs/{ListedJob.select().count() + 1}",
            "company_name": "První Programátorská, a.s.",
            "company_logo_path": "logos-jobs/unknown.webp",
            **kwargs,
        }
    )


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
    return (
        "<!DOCTYPE html>"
        '<html lang="cs"><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="/static/css/index.css">'
        '<script defer src="/static/js/index.js"></script>'
        f"</head><body>{html}</body></html>"
    )


@pytest.fixture(scope="session")
def browser() -> Generator[Browser]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser, static_dir: Path) -> Generator[Page]:
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def serve(page: Page, static_dir: Path) -> Callable[[str], None]:
    """Serves given HTML for any page URL, and the JS/CSS bundle for /static/"""

    def serve(html: str) -> None:
        def handle(route: Route) -> None:
            path = route.request.url.removeprefix(BASE_URL).split("?")[0]
            if path.startswith("/static/"):
                file_path = static_dir / path.removeprefix("/static/")
                if file_path.is_file():
                    route.fulfill(path=file_path)
                else:
                    route.fulfill(status=404)
            else:
                route.fulfill(body=html, content_type="text/html; charset=utf-8")

        page.route(f"{BASE_URL}/**", handle)

    return serve


@pytest.fixture
def jobs_page(test_db: SqliteDatabase, serve: Callable[[str], None]) -> Callable:
    """Renders jobs.jinja from whatever jobs are in the test database"""

    def jobs_page(url: str = "/jobs/", page_meta: dict | None = None) -> None:
        serve(render("jobs.jinja", get_jobs_context(), url, page_meta))

    return jobs_page
