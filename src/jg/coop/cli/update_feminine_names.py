from pathlib import Path

import click
import httpx2
from lxml import html

from jg.coop.lib import loggers
from jg.coop.lib.brand import BOT_USER_AGENT


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


@click.command()
@click.option(
    "--path",
    default=Path("src/jg/coop/data/feminine_names.txt"),
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
)
def main(path: Path):
    """Download the list of Czech feminine names from Wikipedia to a static file"""
    logger.info(f"Downloading {WIKI_URL}")
    response = httpx2.get(WIKI_URL, headers={"User-Agent": BOT_USER_AGENT}, timeout=30)
    response.raise_for_status()
    names = parse_wiki_names(response.text)
    logger.info(f"Parsed {len(names)} names from Wikipedia")
    path.write_text(format_names(names + EXTRA_NAMES))
    logger.info(f"Saved to {path}")


def parse_wiki_names(page_html: str) -> list[str]:
    html_tree = html.fromstring(page_html)
    return [
        element.text_content().strip()
        for element in html_tree.cssselect(".mw-parser-output .wikitable a[href]")
    ]


def format_names(names: list[str]) -> str:
    return "".join(f"{name}\n" for name in sorted(set(names)))
