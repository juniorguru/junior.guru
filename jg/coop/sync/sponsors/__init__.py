from datetime import datetime
from pathlib import Path

import click
from githubkit import GitHub

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.sponsor import GitHubSponsor


SPONSORS_GQL = (Path(__file__).parent / "sponsors.gql").read_text()

GITHUB_USERNAME = "juniorguru"

GITHUB_PERSONAL_USERNAME = "honzajavorek"


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--github-api-key", default=default_from_env("GITHUB_API_KEY"), required=True
)
@db.connection_context()
def main(github_api_key: str):
    db.drop_tables([GitHubSponsor])
    db.create_tables([GitHubSponsor])

    with GitHub(github_api_key) as github:
        data = github.graphql(SPONSORS_GQL, {"login": GITHUB_PERSONAL_USERNAME})
        for node in data["user"]["sponsorshipsAsMaintainer"]["nodes"]:
            logger.info(f"Saving GitHub sponsor {node['sponsorEntity']['login']}")
            GitHubSponsor.create(
                slug=node["sponsorEntity"]["login"],
                name=node["sponsorEntity"]["name"],
                url=node["sponsorEntity"]["url"],
                avatar_url=node["sponsorEntity"]["avatarUrl"],
                sponsored_on=datetime.fromisoformat(node["createdAt"]).date(),
                is_active=node["isActive"],
            )
