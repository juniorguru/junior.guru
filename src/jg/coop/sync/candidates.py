from io import BytesIO
from pathlib import Path

import click
import httpx
from PIL import Image

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.images import create_fallback_image
from jg.coop.lib.location import locate_fuzzy
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate, CandidateProject
from jg.coop.models.club import ClubUser


IMAGE_SAVE_OPTIONS = {
    "format": "WEBP",
    "optimize": True,
    "quality": 80,
    "method": 6,
    "lossless": False,
}

DEFAULT_PROJECT_IMAGE_FILENAME = "default.webp"


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
@click.option("--project-images-dirname", default="projects", type=str)
@db.connection_context()
@async_command
async def main(
    api_url: str,
    images_dir: Path,
    avatars_dirname: str,
    avatar_size_px: int,
    project_images_dirname: str,
):
    logger.debug("Setting up avatars directory")
    avatars_path = images_dir / avatars_dirname
    avatars_path.mkdir(exist_ok=True, parents=True)
    for path in avatars_path.glob("*.webp"):
        path.unlink()

    logger.debug("Setting up project images directory")
    project_images_path = images_dir / project_images_dirname
    project_images_path.mkdir(exist_ok=True, parents=True)
    for path in project_images_path.glob("*.webp"):
        if path.name != DEFAULT_PROJECT_IMAGE_FILENAME:
            path.unlink()
    default_thumbnail_path = str((project_images_path / DEFAULT_PROJECT_IMAGE_FILENAME).relative_to(images_dir))

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
            candidate_item["avatar_is_default"] = any(
                issue
                for issue in candidate_item["issues"]
                if issue["rule"] == "has_avatar" and issue["status"] == "error"
            )
            discord_id = candidate_item.pop("discord_id", None)
            projects_items = candidate_item.pop("projects", [])
            location_raw = candidate_item.pop("location", None)

            candidate = Candidate.create(is_member=False, **candidate_item)
            if discord_id and (user := ClubUser.get_or_none(discord_id)):
                candidate.user = user
                candidate.is_member = user.is_member
                candidate.save()
                logger.info(f"Saved {candidate!r} ↔ {user!r}, member: {user.is_member}")
            else:
                logger.info(f"Saved {candidate!r} ↔ no club user")

            if location_raw:
                candidate.location_raw = location_raw
                location_fuzzy = await locate_fuzzy(location_raw)
                candidate.location_fuzzy = location_fuzzy.model_dump()
                candidate.save()
                logger.info(f"Located {location_raw!r} as {candidate.location_text!r}")

            avatar_path = avatars_path / f"{candidate.github_username}.webp"
            if candidate.avatar_is_default:
                if name := candidate.name:
                    initial = name.split()[-1][0].upper()
                else:
                    initial = "?"
                logger.debug(f"Generating fallback avatar: {initial}")
                create_fallback_image(initial, avatar_size_px).save(
                    avatar_path, **IMAGE_SAVE_OPTIONS
                )
            else:
                logger.debug(f"Downloading avatar: {candidate.avatar_url}")
                response = await client.get(candidate.avatar_url)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                image = image.resize((avatar_size_px, avatar_size_px))
                image.save(avatar_path, **IMAGE_SAVE_OPTIONS)
            candidate.avatar_path = str(avatar_path.relative_to(images_dir))
            candidate.save()
            logger.info(f"Saved avatar: {avatar_path}")

            for project_item in projects_items:
                thumbnail_path = default_thumbnail_path
                if thumbnail_url := project_item.pop("thumbnail_url", None):
                    try:
                        logger.debug(f"Downloading project image: {thumbnail_url}")
                        response = await client.get(thumbnail_url)
                        response.raise_for_status()
                        image_path = project_images_path / Path(thumbnail_url).name
                        image_path.write_bytes(response.content)
                        thumbnail_path = str(image_path.relative_to(images_dir))
                        logger.info(f"Saved project image: {image_path}")
                    except (httpx.HTTPError, OSError) as e:
                        logger.warning(f"Failed to download project image from {thumbnail_url!r}: {type(e).__name__}: {e}")
                        logger.info(f"Using default image for project")
                CandidateProject.create(
                    candidate=candidate,
                    thumbnail_path=thumbnail_path,
                    **project_item,
                )
            logger.info(f"Saved {len(projects_items)} projects for {candidate!r}")
