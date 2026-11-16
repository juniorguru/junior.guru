import json
from collections.abc import Iterable
from datetime import date

from jinja2.utils import htmlsafe_json_dumps
from markupsafe import Markup

from jg.coop.lib import brand


ORGANIZATION_ID = f"{brand.SITE_URL}#organization"

PODCAST_ID = f"{brand.PODCAST_URL}#series"


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
        "name": brand.SITE_NAME,
        "alternateName": brand.SITE_ALTERNATE_NAMES,
        "url": brand.SITE_URL,
        "inLanguage": "cs",
        "publisher": {"@id": ORGANIZATION_ID},
    }


def organization_json_ld() -> dict:
    return {
        "@type": "Organization",
        "@id": ORGANIZATION_ID,
        "name": brand.SITE_NAME,
        "alternateName": brand.SITE_ALTERNATE_NAMES,
        "url": brand.SITE_URL,
        "logo": brand.static_url("logo.png"),
        "founder": {"@type": "Person", "name": brand.FOUNDER_NAME},
        "sameAs": [
            brand.GITHUB_URL,
            brand.INSTAGRAM_URL,
            brand.LINKEDIN_URL,
            brand.TIKTOK_URL,
            brand.YOUTUBE_URL,
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
        "name": brand.PODCAST_NAME,
        "url": brand.PODCAST_URL,
        "inLanguage": "cs",
        "webFeed": brand.PODCAST_FEED_URL,
        "image": brand.PODCAST_IMAGE_URL,
        "sameAs": [
            brand.YOUTUBE_URL,
            brand.PODCAST_SPOTIFY_URL,
            brand.PODCAST_APPLE_URL,
        ],
    }
