import click
import requests

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
@click.option("--api-url", default="https://juniorguru.github.io/eggtray/profiles.json")
@db.connection_context()
def main(api_url: str):
    Candidate.drop_table()
    Candidate.create_table()

    logger.info("Reading API")
    response = requests.get(api_url)
    response.raise_for_status()
    for profile in response.json():
        candidate = Candidate.from_api(profile)
        candidate.save()
        logger.info(f"Saved {candidate.github_username!r} ( ↔ {candidate.user!r})")
