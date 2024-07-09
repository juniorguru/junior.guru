from datetime import date
from pathlib import Path

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.members import Members


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--history-path",
    default="jg/coop/data/members.jsonl",
    type=click.Path(path_type=Path),
)
@db.connection_context()
def main(history_path: Path):
    logger.info("Preparing database")
    Members.drop_table()
    Members.create_table()

    logger.info("Reading history from a file")
    history_path.touch(exist_ok=True)
    with history_path.open() as f:
        for line in f:
            Members.deserialize(line)

    month = f"{date.today():%Y-%m}"
    logger.info(f"Current month: {month}")

    # FROM 1ST OF MONTH TO END OF THE MONTH:
    # all active members (discord yes/no)
    # number of trial users
    # number of trial-to-paid users
    # active members with an individual plan (monthly/annual)
    # active members with a sponsorship group plan
    # active members with a partnership group plan
    # active members with an internal group plan (finaid, staff, etc.)
    # signups on individual plan
    # quits on individual plan
    # active members with feminine names
    #
    # (conversion rate of trial members to individual plan)
    # (churn of leaving members on individual plan)
    # Dél­ka se­tr­vá­ní v klubu - zrušit

    logger.info("Saving history to a file")
    with history_path.open("w") as f:
        for db_object in Members.history():
            f.write(db_object.serialize())
