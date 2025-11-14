import asyncio
from pprint import pp

import click

from jg.coop.lib import loggers, mutations
from jg.coop.lib.location import locate, locate_fuzzy


logger = loggers.from_path(__file__)


@click.command()
@click.argument("location_raw")  # e.g. 'Ústí nad Orlicí, Pardubice, Czechia'
@click.option("--fuzzy/--no-fuzzy", is_flag=True, default=False)
def main(location_raw: str, fuzzy: bool):
    if fuzzy:
        mutations.allow("openai")
        pp(asyncio.run(locate_fuzzy(location_raw)))
    else:
        pp(asyncio.run(locate(location_raw)))
