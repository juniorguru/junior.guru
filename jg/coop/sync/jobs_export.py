import itertools
import json
from pathlib import Path

import click
import httpx

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers
from jg.coop.models.base import db


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--output-dir",
    default=Path("jg/coop/data/jobs"),
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True, writable=True),
)
@db.connection_context()
def main(output_dir: Path):
    actor_names = [
        actor_name
        for actor_name in apify.fetch_scheduled_actors()
        if actor_name.startswith("honzajavorek/jobs-")
    ]
    logger.info(f"Found {len(actor_names)} actors: {actor_names}")
    items = itertools.chain.from_iterable(
        apify.fetch_data(actor_name, raise_if_missing=False)
        for actor_name in actor_names
    )
    logger.info("Fetched all items")

    output_dir.mkdir(parents=True, exist_ok=True)
    api_file = output_dir / "jobs.jsonl"
    with api_file.open(mode="w") as f:
        for item in items:
            line = json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n"
            f.write(line)
    logger.info(f"Saved items to {api_file}")

    logger.info("Fetching schema file from GitHub")
    response = httpx.get(
        "https://raw.githubusercontent.com/"
        "juniorguru/plucker"  # repo
        "/refs/heads/main/"
        "jg/plucker/schemas/jobSchema.json",  # path
        follow_redirects=True,
    )
    response.raise_for_status()
    schema_file = output_dir / "schema-apify.json"
    schema_file.write_bytes(response.content)
    logger.info(f"Saved schema to {schema_file}")
