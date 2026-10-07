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
from playwright.sync_api import Browser, Page, Route, expect, sync_playwright

from jg.coop.lib import template_filters
from jg.coop.lib.location import REGIONS
from jg.coop.lib.mkdocs_jinja import get_filters
from jg.coop.models.club import ClubUser
from jg.coop.models.job import DiscordJob, ListedJob
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


def create_job(regions: list[str] | None = None, **kwargs) -> ListedJob:
    title = kwargs.pop("title", "Junior Developer")
    if regions:
        kwargs["locations"] = [create_location(region) for region in regions]
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


def create_location(region: str) -> dict[str, str]:
    if region not in REGIONS:
        raise ValueError(f"Unknown region: {region}")
    return {"raw": region, "place": region, "region": region, "country_code": "CZ"}


def create_discord_job(**kwargs) -> DiscordJob:
    author, _ = ClubUser.get_or_create(
        id=1, defaults={"display_name": "Kuře Žluté", "mention": "<@1>"}
    )
    number = DiscordJob.select().count() + 1
    return DiscordJob.create(
        **{
            "title": "Junior Developer from Discord",
            "author": author,
            "posted_on": date(2026, 1, 1),
            "description_discord": "Junior Developer from Discord",
            "url": f"https://discord.com/channels/1/2/{number}",
            "upvotes_count": 0,
            "comments_count": 0,
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


# Module scope, because the sync Playwright API keeps an event loop running,
# which would break any async tests executed while the browser is open
@pytest.fixture(scope="module")
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
