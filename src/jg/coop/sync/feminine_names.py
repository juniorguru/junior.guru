import unicodedata
from pathlib import Path

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.feminine_name import FeminineName


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--path",
    default=Path("src/jg/coop/data/feminine_names.txt"),
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@db.connection_context()
def main(path: Path):
    """Fill the table with feminine names from a static file

    The file has been originally scraped from https://cs.wikipedia.org/wiki/Seznam_nej%C4%8Dast%C4%9Bj%C5%A1%C3%ADch_%C5%BEensk%C3%BDch_jmen_v_%C4%8Cesku
    and extended with extra names.
    """
    FeminineName.drop_table()
    FeminineName.create_table()
    names = parse_names(path.read_text())
    variants = get_variants(names)
    logger.info(f"Loaded {len(names)} names, {len(variants)} variants")
    FeminineName.insert_many([{"name": name} for name in variants]).execute()


def parse_names(text: str) -> list[str]:
    return [name for line in text.splitlines() if (name := line.strip())]


def get_variants(names: list[str]) -> list[str]:
    variants = {}
    for name in names:
        name_lower = name.lower()
        variants[name_lower] = True
        variants[remove_accents(name_lower)] = True
    return list(variants)


def remove_accents(s: str) -> str:
    # https://stackoverflow.com/a/518232/325365
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )
