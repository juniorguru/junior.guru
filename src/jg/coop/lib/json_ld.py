import json
from collections.abc import Iterable
from datetime import date

from jinja2.utils import htmlsafe_json_dumps

from jg.coop.lib.social import GITHUB_URL, LINKEDIN_URL, YOUTUBE_URL


SITE_URL = "https://junior.guru/"

SITE_NAME = "junior.guru"

SITE_ALTERNATE_NAMES = ["Junior Guru"]

ORGANIZATION_ID = f"{SITE_URL}#organization"


def dumps(data: dict) -> str:
    """Serializes structured data so that it's safe to embed in a <script> tag."""
    data = {"@context": "https://schema.org"} | data
    return str(
        htmlsafe_json_dumps(data, dumps=json.dumps, ensure_ascii=False, sort_keys=True)
    )


def website_json_ld() -> str:
    return dumps(
        {
            "@type": "WebSite",
            "name": SITE_NAME,
            "alternateName": SITE_ALTERNATE_NAMES,
            "url": SITE_URL,
            "inLanguage": "cs",
            "publisher": {"@id": ORGANIZATION_ID},
        }
    )


def organization_json_ld() -> str:
    return dumps(
        {
            "@type": "Organization",
            "@id": ORGANIZATION_ID,
            "name": SITE_NAME,
            "alternateName": SITE_ALTERNATE_NAMES,
            "url": SITE_URL,
            "logo": f"{SITE_URL}static/logo.png",
            "founder": {"@type": "Person", "name": "Honza Javorek"},
            "sameAs": [GITHUB_URL, LINKEDIN_URL, YOUTUBE_URL],
        }
    )


def breadcrumb_list_json_ld(items: Iterable[tuple[str, str]]) -> str:
    return dumps(
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": position, "name": name, "item": url}
                for position, (name, url) in enumerate(items, start=1)
            ],
        }
    )


def article_json_ld(
    headline: str,
    url: str,
    published_on: date,
    author_name: str,
    author_url: str | None = None,
    image_url: str | None = None,
) -> str:
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
    return dumps(data)
