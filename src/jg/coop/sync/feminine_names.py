import unicodedata

import httpx
from lxml import html

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.feminine_name import FeminineName


logger = loggers.from_path(__file__)


# https://cs.wikipedia.org/wiki/Seznam_nej%C4%8Dast%C4%9Bj%C5%A1%C3%ADch_%C5%BEensk%C3%BDch_jmen_v_%C4%8Cesku
WIKI_PAGE_TITLE = "Seznam nejčastějších ženských jmen v Česku"

WIKI_API_URL = "https://cs.wikipedia.org/w/api.php"

EXTRA_NAMES = [
    "Alisa",
    "Anastasija",
    "Anastassiya",
    "Darja",
    "Dinara",
    "Eleanor",
    "Evgenia",
    "Hannah",
    "Hany",
    "Katarína",
    "Kate",
    "Kayla",
    "Lindice",
    "Lívia",
    "Nataliya",
    "Oxana",
    "Rozvita",
    "Tina",
]


@cli.sync_command()
@db.connection_context()
def main():
    FeminineName.drop_table()
    FeminineName.create_table()

    response = httpx.get(
        WIKI_API_URL,
        params={
            "action": "parse",
            "page": WIKI_PAGE_TITLE,
            "prop": "text",
            "format": "json",
        },
        headers={"User-Agent": "JuniorGuruBot (+https://junior.guru)"},
    )
    response.raise_for_status()
    data = response.json()

    page_html = data["parse"]["text"]["*"]
    html_tree = html.fromstring(page_html)

    names = [
        element.text_content().strip()
        for element in html_tree.cssselect(".wikitable a[href]")
    ] + EXTRA_NAMES

    for name in names:
        name_lower = name.lower()
        name_ascii = remove_accents(name_lower)
        logger.info(f"{name} → {name_lower}, {name_ascii}")
        FeminineName.insert_many(
            [
                dict(name=name_lower),
                dict(name=name_ascii),
            ]
        ).on_conflict_ignore().execute()


def remove_accents(s):
    # https://stackoverflow.com/a/518232/325365
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )
