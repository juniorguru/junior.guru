from datetime import date
from pathlib import Path

import click
import yaml
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.brand import podcast_media_url
from jg.coop.lib.images import is_image, validate_image
from jg.coop.models.base import db
from jg.coop.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


IMAGES_DIR = Path("src/jg/coop/images")

AVATARS_DIR = IMAGES_DIR / "avatars-participants"

MEDIA_TYPE = "audio/mpeg"


class PodcastEpisodeConfig(BaseModel):
    number: int
    title: str
    guest_name: str | None = None
    guest_has_feminine_name: bool | None = None
    guest_affiliation: str | None = None
    publish_on: date
    description: str
    image_path: str
    media_size: int
    media_duration_s: int


@cli.sync_command()
@click.option(
    "--path",
    default=Path("src/jg/coop/data/podcast.yml"),
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@db.connection_context()
def main(path: Path):
    logger.info("Validating avatar images")
    for avatar_path in filter(is_image, AVATARS_DIR.glob("*.*")):
        logger.debug(f"Validating {avatar_path}")
        validate_image(avatar_path)

    logger.info("Setting up podcast episodes db table")
    PodcastEpisode.drop_table()
    PodcastEpisode.create_table()

    logger.info("Reading YAML with episodes")
    for yaml_record in yaml.safe_load(path.read_text()):
        record = parse_episode(PodcastEpisodeConfig(**yaml_record))
        if not (IMAGES_DIR / record["image_path"]).exists():
            raise ValueError(
                f"Episode #{record['number']} references {record['image_path']}, but it doesn't exist"
            )
        logger.info(f"Saving episode #{record['number']}")
        PodcastEpisode.create(**record)


def parse_episode(config: PodcastEpisodeConfig) -> dict:
    """Turns episode configuration into a record for the database"""
    if config.guest_name:
        if config.guest_has_feminine_name is None:
            raise ValueError(
                f"Episode #{config.number} is missing guest_has_feminine_name"
            )
    elif config.guest_affiliation or config.guest_has_feminine_name is not None:
        raise ValueError(f"Episode #{config.number} is missing guest_name")

    media_slug = f"{config.number:04d}"
    return {
        "number": config.number,
        "publish_on": config.publish_on,
        "title": config.title,
        "guest_name": config.guest_name,
        "guest_has_feminine_name": config.guest_has_feminine_name,
        "guest_affiliation": config.guest_affiliation,
        "image_path": config.image_path,
        "description": config.description,
        "media_slug": media_slug,
        "media_url": podcast_media_url(media_slug),
        "media_size": config.media_size,
        "media_type": MEDIA_TYPE,
        "media_duration_s": config.media_duration_s,
    }
