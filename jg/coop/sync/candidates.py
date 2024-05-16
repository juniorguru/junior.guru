import click
import requests

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate, CandidateProject


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
@click.option("--api-url", default="https://juniorguru.github.io/eggtray/profiles.json")
@db.connection_context()
def main(api_url: str):
    db.drop_tables([Candidate, CandidateProject])
    db.create_tables([Candidate, CandidateProject])

    logger.info("Reading API")
    response = requests.get(api_url)
    response.raise_for_status()

    for candidate_item in response.json()["items"]:
        discord_id = candidate_item.pop("discord_id", None)
        projects_items = candidate_item.pop("projects", [])

        candidate = Candidate.create(user=discord_id, is_member=False, **candidate_item)
        if candidate.user:
            candidate.is_member = candidate.user.is_member
            candidate.save()
        logger.info(f"Saved {candidate!r} ( ↔ {candidate.user!r})")

        for project_item in projects_items:
            CandidateProject.create(candidate=candidate, **project_item)
        logger.info(f"Saved {len(projects_items)} projects for {candidate!r}")
