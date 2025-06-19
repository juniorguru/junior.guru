import unicodedata

import requests
from lxml import html

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.feminine_name import FeminineName


logger = loggers.from_path(__file__)


WIKI_URL = "https://cs.wikipedia.org/wiki/Seznam_nej%C4%8Dast%C4%9Bj%C5%A1%C3%ADch_%C5%BEensk%C3%BDch_jmen_v_%C4%8Cesku"

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

    response = requests.get(WIKI_URL)
    response.raise_for_status()
    html_tree = html.fromstring(response.content)

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
