import json
from datetime import date

import pytest

from jg.coop.lib import json_ld


FAQ_HTML = """
<h1>Klub: Otázky a odpovědi</h1>
<div class="lead"><p>Intro</p></div>
<div class="document-toc"><ul><li><a href="#q1">Jak funguje členství?</a></li></ul></div>
<h2 id="q1">Jak funguje členství?<a class="headerlink" href="#q1" title="Odkaz na tuto sekci">#</a></h2>
<p>Dokud máš <a href="https://discord.com/">aktivní</a> předplatné.</p>
<p>Druhý
  odstavec.</p>
<h2 id="q2">Proč zrovna Discord?<a class="headerlink" href="#q2">#</a></h2>
<ul><li>Hlasové kanály</li></ul>
"""


def test_dumps_adds_context():
    data = json.loads(json_ld.dumps({"@type": "Thing"}))

    assert data == {"@context": "https://schema.org", "@type": "Thing"}


def test_dumps_escapes_script_closing_tag():
    assert "</script>" not in json_ld.dumps({"name": "</script><script>"})


def test_dumps_keeps_unicode():
    assert "Otázky" in json_ld.dumps({"name": "Otázky"})


def test_website():
    data = json.loads(json_ld.website())

    assert data["@type"] == "WebSite"
    assert data["name"] == "junior.guru"
    assert data["alternateName"] == ["Junior Guru"]
    assert data["url"] == "https://junior.guru/"


def test_website_publisher_references_organization():
    website = json.loads(json_ld.website())
    organization = json.loads(json_ld.organization())

    assert website["publisher"]["@id"] == organization["@id"]


def test_podcast_series():
    data = json.loads(json_ld.podcast_series())

    assert data["@type"] == "PodcastSeries"
    assert data["url"] == "https://junior.guru/podcast/"


def test_breadcrumb_list():
    data = json.loads(
        json_ld.breadcrumb_list(
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
        json_ld.article(
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
        json_ld.article(
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


def test_parse_faq():
    assert json_ld.parse_faq(FAQ_HTML) == [
        ("Jak funguje členství?", "Dokud máš aktivní předplatné.\n\nDruhý odstavec."),
        ("Proč zrovna Discord?", "Hlasové kanály"),
    ]


def test_faq_page():
    data = json.loads(json_ld.faq_page(FAQ_HTML))

    assert data["mainEntity"][0] == {
        "@type": "Question",
        "name": "Jak funguje členství?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Dokud máš aktivní předplatné.\n\nDruhý odstavec.",
        },
    }
