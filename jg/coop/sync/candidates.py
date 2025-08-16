import click
import requests

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate, CandidateProject
from jg.coop.models.club import ClubUser


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
        logger.debug(f"Candidate {candidate_item!r}")
        discord_id = candidate_item.pop("discord_id", None)
        projects_items = candidate_item.pop("projects", [])

        candidate = Candidate.create(is_member=False, **candidate_item)
        if discord_id and (user := ClubUser.get_or_none(discord_id)):
            candidate.user = user
            candidate.is_member = user.is_member
            candidate.save()
            logger.info(f"Saved {candidate!r} ( ↔ {user!r})")
        else:
            logger.info(f"Saved {candidate!r} (no club user)")

        for project_item in projects_items:
            CandidateProject.create(candidate=candidate, **project_item)
        logger.info(f"Saved {len(projects_items)} projects for {candidate!r}")
