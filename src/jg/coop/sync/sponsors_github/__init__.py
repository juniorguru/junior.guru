from io import BytesIO
from pathlib import Path

import click
import requests
from githubkit import GitHub
from PIL import Image

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.sponsor import GitHubSponsor


SPONSORS_GQL = (Path(__file__).parent / "sponsors.gql").read_text()

GITHUB_USERNAME = "juniorguru"

GITHUB_PERSONAL_USERNAME = "honzajavorek"

IMAGES_PATH = Path("jg/coop/images")

AVATARS_PATH = IMAGES_PATH / "avatars-sponsors"

AVATAR_SIZE_PX = 120


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--github-api-key", default=default_from_env("GITHUB_API_KEY"), required=True
)
@db.connection_context()
def main(github_api_key: str):
    GitHubSponsor.drop_table()
    GitHubSponsor.create_table()

    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob("*.png"):
        path.unlink()

    with GitHub(github_api_key) as github:
        data = github.graphql(SPONSORS_GQL, {"login": GITHUB_PERSONAL_USERNAME})
        for node in data["user"]["sponsorshipsAsMaintainer"]["nodes"]:
            sponsor_slug = node["sponsorEntity"]["login"]
            avatar_url = node["sponsorEntity"]["avatarUrl"]

            logger.info(f"Downloading avatar {avatar_url}")
            response = requests.get(avatar_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image.thumbnail((AVATAR_SIZE_PX, AVATAR_SIZE_PX))
            image_path = AVATARS_PATH / f"{sponsor_slug}.png"
            image.save(image_path, "PNG")
            avatar_path = str(image_path.relative_to(IMAGES_PATH))

            logger.info(f"Saving GitHub sponsor {node['sponsorEntity']['login']}")
            GitHubSponsor.create(
                slug=sponsor_slug,
                name=node["sponsorEntity"]["name"],
                url=node["sponsorEntity"]["url"],
                avatar_path=avatar_path,
                is_active=node["isActive"],
            )

    logger.info(f"Saved {GitHubSponsor.count()} GitHub sponsors")
