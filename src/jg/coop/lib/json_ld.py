import json
from collections.abc import Iterable
from datetime import date

from jinja2.utils import htmlsafe_json_dumps
from markupsafe import Markup

from jg.coop.lib.brand import (
    FOUNDER_NAME,
    GITHUB_URL,
    INSTAGRAM_URL,
    LINKEDIN_URL,
    PODCAST_APPLE_URL,
    PODCAST_FEED_URL,
    PODCAST_IMAGE_URL,
    PODCAST_NAME,
    PODCAST_SPOTIFY_URL,
    PODCAST_URL,
    SITE_ALTERNATE_NAMES,
    SITE_NAME,
    SITE_URL,
    TIKTOK_URL,
    YOUTUBE_URL,
    static_url,
)


ORGANIZATION_ID = f"{SITE_URL}#organization"

PODCAST_ID = f"{PODCAST_URL}#series"


def dumps(data: dict) -> Markup:
    """Serializes structured data so that it's safe to embed in a <script> tag"""
    data = {"@context": "https://schema.org"} | data
    return htmlsafe_json_dumps(
        data, dumps=json.dumps, ensure_ascii=False, sort_keys=True
    )


def graph_json_ld(*nodes: dict) -> dict:
    """Combines several nodes, linked by their @id, into one JSON-LD document"""
    return {"@graph": list(nodes)}


def website_json_ld() -> dict:
    return {
        "@type": "WebSite",
        "name": SITE_NAME,
        "alternateName": SITE_ALTERNATE_NAMES,
        "url": SITE_URL,
        "inLanguage": "cs",
        "publisher": {"@id": ORGANIZATION_ID},
    }


def organization_json_ld() -> dict:
    return {
        "@type": "Organization",
        "@id": ORGANIZATION_ID,
        "name": SITE_NAME,
        "alternateName": SITE_ALTERNATE_NAMES,
        "url": SITE_URL,
        "logo": static_url("logo.png"),
        "founder": {"@type": "Person", "name": FOUNDER_NAME},
        "sameAs": [
            GITHUB_URL,
            INSTAGRAM_URL,
            LINKEDIN_URL,
            TIKTOK_URL,
            YOUTUBE_URL,
        ],
    }


def breadcrumb_list_json_ld(items: Iterable[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": position, "name": name, "item": url}
            for position, (name, url) in enumerate(items, start=1)
        ],
    }


def article_json_ld(
    headline: str,
    url: str,
    published_on: date,
    author_name: str,
    author_url: str | None = None,
    image_url: str | None = None,
) -> dict:
    author = {"@type": "Person", "name": author_name}
    if author_url:
        author["url"] = author_url
    data = {
        "@type": "Article",
        "headline": headline,
        "url": url,
        "datePublished": published_on.isoformat(),
        "author": author,
        "publisher": {"@id": ORGANIZATION_ID},
        "inLanguage": "cs",
    }
    if image_url:
        data["image"] = image_url
    return data


def podcast_series_json_ld() -> dict:
    return {
        "@type": "PodcastSeries",
        "@id": PODCAST_ID,
        "name": PODCAST_NAME,
        "url": PODCAST_URL,
        "inLanguage": "cs",
        "webFeed": PODCAST_FEED_URL,
        "image": PODCAST_IMAGE_URL,
        "sameAs": [YOUTUBE_URL, PODCAST_SPOTIFY_URL, PODCAST_APPLE_URL],
    }
