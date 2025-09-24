from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.job import DiscordJob, DroppedJob, JobStats, ListedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-club"])
@click.option(
    "--history-path",
    default="src/jg/coop/data/jobs.jsonl",
    type=click.Path(path_type=Path),
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
def main(history_path: Path, today: date):
    monday = today - timedelta(days=today.weekday())
    logger.info(f"The closest Monday: {monday}")

    JobStats.drop_table()
    JobStats.create_table()

    logger.info("Reading stats history")
    history_path.touch(exist_ok=True)
    with history_path.open() as f:
        for line in f:
            JobStats.deserialize(line)

    logger.info("Calculating stats")
    tech = defaultdict(int)
    for job in ListedJob.listing():
        for tag in job.tech_tags or []:
            tech[tag] += 1
    JobStats.add(
        day=monday,
        scraped_count=ListedJob.count(),
        discord_count=DiscordJob.count(),
        dropped_count=DroppedJob.count(),
        tech=dict(tech),
    )

    logger.info("Updating stats")
    with history_path.open("w") as f:
        for db_object in JobStats.history():
            f.write(db_object.serialize())
