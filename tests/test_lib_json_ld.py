import json
from datetime import date

import pytest

from jg.coop.lib import json_ld


def test_dumps_adds_context():
    data = json.loads(json_ld.dumps({"@type": "Thing"}))

    assert data == {"@context": "https://schema.org", "@type": "Thing"}


def test_dumps_escapes_html():
    assert "<" not in json_ld.dumps({"name": "</script><script>"})


def test_dumps_escaped_html_round_trips():
    data = json.loads(json_ld.dumps({"name": "</script>&'"}))

    assert data["name"] == "</script>&'"


def test_dumps_keeps_unicode():
    assert "Otázky" in json_ld.dumps({"name": "Otázky"})


def test_website():
    data = json.loads(json_ld.website_json_ld())

    assert data["@type"] == "WebSite"
    assert data["name"] == "junior.guru"
    assert data["alternateName"] == ["Junior Guru"]
    assert data["url"] == "https://junior.guru/"


def test_website_publisher_references_organization():
    website = json.loads(json_ld.website_json_ld())
    organization = json.loads(json_ld.organization_json_ld())

    assert website["publisher"]["@id"] == organization["@id"]


def test_breadcrumb_list():
    data = json.loads(
        json_ld.breadcrumb_list_json_ld(
            [
                ("Příběhy", "https://junior.guru/stories/"),
                ("Elvíra Krieger", "https://junior.guru/stories/elvira-krieger/"),
            ]
        )
    )

    assert data["itemListElement"] == [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Příběhy",
            "item": "https://junior.guru/stories/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Elvíra Krieger",
            "item": "https://junior.guru/stories/elvira-krieger/",
        },
    ]


def test_article():
    data = json.loads(
        json_ld.article_json_ld(
            headline="Do IT bez titulu",
            url="https://junior.guru/stories/elvira-krieger/",
            published_on=date(2026, 4, 9),
            author_name="Adéla Pavlun",
            author_url="https://www.linkedin.com/in/adelapavlun/",
            image_url="https://junior.guru/static/thumbnail.png",
        )
    )

    assert data == {
        "@context": "https://schema.org",
        "@type": "Article",
        "author": {
            "@type": "Person",
            "name": "Adéla Pavlun",
            "url": "https://www.linkedin.com/in/adelapavlun/",
        },
        "datePublished": "2026-04-09",
        "headline": "Do IT bez titulu",
        "image": "https://junior.guru/static/thumbnail.png",
        "inLanguage": "cs",
        "publisher": {"@id": "https://junior.guru/#organization"},
        "url": "https://junior.guru/stories/elvira-krieger/",
    }


@pytest.mark.parametrize("key", ["image", "author.url"])
def test_article_optional_fields(key: str):
    data = json.loads(
        json_ld.article_json_ld(
            headline="Do IT bez titulu",
            url="https://junior.guru/stories/elvira-krieger/",
            published_on=date(2026, 4, 9),
            author_name="Adéla Pavlun",
        )
    )
    *parents, name = key.split(".")
    for parent in parents:
        data = data[parent]

    assert name not in data
