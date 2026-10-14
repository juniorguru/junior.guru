import json
import re
from collections.abc import Iterable
from datetime import date

from bs4 import BeautifulSoup, Tag


SITE_URL = "https://junior.guru/"

SITE_NAME = "junior.guru"

SITE_ALTERNATE_NAMES = ["Junior Guru"]

PODCAST_URL = "https://junior.guru/podcast/"

PODCAST_NAME = "Junior Guru: programování a kariéra v IT"


def dumps(data: dict) -> str:
    """Serializes structured data so that it's safe to embed in a <script> tag."""
    data = {"@context": "https://schema.org"} | data
    return json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")


def website() -> str:
    return dumps(
        {
            "@type": "WebSite",
            "name": SITE_NAME,
            "alternateName": SITE_ALTERNATE_NAMES,
            "url": SITE_URL,
            "inLanguage": "cs",
            "publisher": {"@id": f"{SITE_URL}#organization"},
        }
    )


def organization() -> str:
    return dumps(
        {
            "@type": "Organization",
            "@id": f"{SITE_URL}#organization",
            "name": SITE_NAME,
            "alternateName": SITE_ALTERNATE_NAMES,
            "url": SITE_URL,
            "logo": f"{SITE_URL}static/logo.png",
            "founder": {"@type": "Person", "name": "Honza Javorek"},
            "sameAs": [
                "https://github.com/juniorguru/",
                "https://www.youtube.com/@juniordotguru",
            ],
        }
    )


def podcast_series() -> str:
    return dumps(
        {
            "@type": "PodcastSeries",
            "@id": f"{PODCAST_URL}#series",
            "name": PODCAST_NAME,
            "url": PODCAST_URL,
            "inLanguage": "cs",
            "webFeed": f"{SITE_URL}api/podcast.xml",
            "image": f"{SITE_URL}static/podcast-v1.png",
            "sameAs": [
                "https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA",
                "https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4",
                "https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549",
            ],
        }
    )


def breadcrumb_list(items: Iterable[tuple[str, str]]) -> str:
    return dumps(
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": position, "name": name, "item": url}
                for position, (name, url) in enumerate(items, start=1)
            ],
        }
    )


def article(
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
        "publisher": {"@id": f"{SITE_URL}#organization"},
        "inLanguage": "cs",
    }
    if image_url:
        data["image"] = image_url
    return dumps(data)


def faq_page(html: str) -> str:
    return dumps(
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {"@type": "Answer", "text": answer},
                }
                for question, answer in parse_faq(html)
            ],
        }
    )


def parse_faq(html: str) -> list[tuple[str, str]]:
    """Reads questions from <h2> headings and answers from what follows them."""
    soup = BeautifulSoup(html, "html.parser")
    for permalink in soup.select(".headerlink"):
        permalink.decompose()
    return [
        (get_text(heading), get_answer_text(heading)) for heading in soup.find_all("h2")
    ]


def get_answer_text(heading: Tag) -> str:
    texts = []
    for sibling in heading.find_next_siblings():
        if sibling.name == "h2":
            break
        if text := get_text(sibling):
            texts.append(text)
    return "\n\n".join(texts)


def get_text(tag: Tag) -> str:
    return re.sub(r"\s+", " ", tag.get_text()).strip()
