from pathlib import Path
from pprint import pprint

import click
from githubkit import GitHub

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.models.base import db


SPONSORS_GQL = (Path(__file__).parent / "sponsors.gql").read_text()

SPONSORS_VALUE_GQL = (Path(__file__).parent / "sponsors_value.gql").read_text()

GITHUB_USERNAME = "juniorguru"

GITHUB_PERSONAL_USERNAME = "honzajavorek"


@cli.sync_command()
@click.option(
    "--github-api-key", default=default_from_env("GITHUB_API_KEY"), required=True
)
@db.connection_context()
def main(github_api_key: str):
    with GitHub(github_api_key) as github:
        data = github.graphql(SPONSORS_GQL, {"login": GITHUB_PERSONAL_USERNAME})
        sponsors = {
            node["sponsorEntity"]["login"]: node["sponsorEntity"]
            for node in data["user"]["sponsorshipsAsMaintainer"]["nodes"]
        }
        pprint(sponsors)

        data = github.graphql(SPONSORS_VALUE_GQL, {"login": GITHUB_PERSONAL_USERNAME})
        for node in data["user"]["lifetimeReceivedSponsorshipValues"]["nodes"]:
            sponsors[node["sponsor"]["login"]]["amountInCents"] = node["amountInCents"]

        pprint(sponsors)
