from io import BytesIO
from pathlib import Path

import click
import httpx
from PIL import Image

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.images import create_fallback_image
from jg.coop.lib.mapycz import locate, repr_locations
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate, CandidateProject
from jg.coop.models.club import ClubUser


IMAGE_SAVE_OPTIONS = {"format": "WEBP", "optimize": True}


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
@click.option("--api-url", default="https://juniorguru.github.io/eggtray/profiles.json")
@click.option(
    "--images-dir",
    default="src/jg/coop/images",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
)
@click.option("--avatars-dirname", default="avatars-candidates", type=str)
@click.option("--avatar-size", "avatar_size_px", default=460, type=int)
@db.connection_context()
@async_command
async def main(
    api_url: str, images_dir: Path, avatars_dirname: str, avatar_size_px: int
):
    logger.debug("Setting up avatars directory")
    avatars_path = images_dir / avatars_dirname
    avatars_path.mkdir(exist_ok=True, parents=True)
    for path in avatars_path.glob("*.webp"):
        path.unlink()

    logger.debug("Setting up database")
    db.drop_tables([Candidate, CandidateProject])
    db.create_tables([Candidate, CandidateProject])

    logger.info("Reading API")
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()

        for candidate_item in data["items"]:
            logger.debug(f"Candidate {candidate_item!r}")
            discord_id = candidate_item.pop("discord_id", None)
            projects_items = candidate_item.pop("projects", [])

            if location_raw := candidate_item.pop("location", None):
                candidate_item["location_raw"] = location_raw
                location = await locate(location_raw)
                candidate_item["location"] = location.model_dump()
                candidate_item["location_repr"] = repr_locations([location])

            github_username = candidate_item["github_username"]
            avatar_path = avatars_path / f"{github_username}.webp"

            if has_avatar(candidate_item):
                avatar_url = candidate_item["avatar_url"]
                logger.debug(f"Downloading avatar: {avatar_url}")
                response = await client.get(avatar_url)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                image = image.resize((avatar_size_px, avatar_size_px))
                image.save(avatar_path, **IMAGE_SAVE_OPTIONS)
            else:
                if name := candidate_item.get("name"):
                    initial = name.split()[-1][0].upper()
                else:
                    initial = "?"
                logger.debug(f"Generating fallback avatar: {initial}")
                create_fallback_image(initial, avatar_size_px).save(
                    avatar_path, **IMAGE_SAVE_OPTIONS
                )
            logger.debug(f"Avatar: {avatar_path}")
            candidate_item["avatar_path"] = str(avatar_path.relative_to(images_dir))

            candidate = Candidate.create(is_member=False, **candidate_item)
            if discord_id and (user := ClubUser.get_or_none(discord_id)):
                candidate.user = user
                candidate.is_member = user.is_member
                candidate.save()
                logger.info(f"Saved {candidate!r} ↔ {user!r}, member: {user.is_member}")
            else:
                logger.info(f"Saved {candidate!r} ↔ no club user")

            for project_item in projects_items:
                CandidateProject.create(candidate=candidate, **project_item)
            logger.info(f"Saved {len(projects_items)} projects for {candidate!r}")


def has_avatar(item: dict) -> bool:
    return not any(
        issue
        for issue in item["issues"]
        if issue["rule"] == "has_avatar" and issue["status"] == "error"
    )
