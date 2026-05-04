import logging
from collections import defaultdict
from datetime import date, timedelta
from io import BytesIO
from pathlib import Path
from pprint import pformat

import click
import httpx
from githubkit import GitHub
from PIL import Image
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cache import cache
from jg.coop.lib.cli import async_command
from jg.coop.lib.images import create_fallback_image
from jg.coop.lib.location import locate_fuzzy
from jg.coop.models.base import db
from jg.coop.models.candidate import (
    Candidate,
    CandidateProject,
    CandidateStats,
    CandidateStatsName,
)
from jg.coop.models.club import ClubUser
from jg.coop.models.feminine_name import FeminineName


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
    "--github-api-key", default=default_from_env("GITHUB_API_KEY"), required=True
)
@click.option(
    "--history-path",
    default="src/jg/coop/data/candidates.jsonl",
    type=click.Path(path_type=Path),
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
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
    github_api_key: str,
    history_path: Path,
    today: date,
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
    default_thumbnail_path = project_images_path / DEFAULT_PROJECT_IMAGE_FILENAME
    default_thumbnail_path = str(default_thumbnail_path.relative_to(images_dir))

    logger.debug("Setting up database")
    db.drop_tables([Candidate, CandidateProject, CandidateStats])
    db.create_tables([Candidate, CandidateProject, CandidateStats])

    month = f"{today:%Y-%m}"
    logger.info(f"Reading stats history, current month: {month}")
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.touch(exist_ok=True)
    with history_path.open() as f:
        for line in f:
            CandidateStats.deserialize(line)

    logger.info("Reading API")
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()

        for candidate_item in data["items"]:
            logger.debug(f"Candidate {pformat(candidate_item)}")
            candidate_item["avatar_is_default"] = any(
                issue
                for issue in candidate_item["issues"]
                if issue["rule"] == "has_avatar" and issue["status"] == "error"
            )
            discord_id = candidate_item.pop("discord_id", None)
            projects_items = candidate_item.pop("projects", [])
            location_raw = candidate_item.pop("location", None)

            candidate = Candidate.create(
                is_member=False,
                has_feminine_name=FeminineName.is_feminine(candidate_item["name"]),
                **candidate_item,
            )
            if discord_id and (user := ClubUser.find_by_id(discord_id)):
                logger.debug(f"Found {user!r}, member: {user.is_member}")
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
                image_bytes = await download_image(client, candidate.avatar_url)
                image = Image.open(BytesIO(image_bytes))
                image = image.resize((avatar_size_px, avatar_size_px))
                image.save(avatar_path, **IMAGE_SAVE_OPTIONS)
            candidate.avatar_path = str(avatar_path.relative_to(images_dir))
            candidate.save()
            logger.info(f"Saved avatar: {avatar_path}")

            for project_item in projects_items:
                if thumbnail_url := project_item.pop("thumbnail_url", None):
                    logger.debug(f"Downloading project image: {thumbnail_url}")
                    image_bytes = await download_image(client, thumbnail_url)
                    image_path = project_images_path / Path(thumbnail_url).name
                    image_path.write_bytes(image_bytes)
                    thumbnail_path = str(image_path.relative_to(images_dir))
                    logger.info(f"Saved project image: {image_path}")
                else:
                    thumbnail_path = default_thumbnail_path
                CandidateProject.create(
                    candidate=candidate,
                    thumbnail_path=thumbnail_path,
                    **project_item,
                )
            logger.info(f"Saved {len(projects_items)} projects for {candidate!r}")

    logger.info("Getting checks stats from GitHub")
    checks_by_month = fetch_github_checks(github_api_key)
    for checks_month, checks_count in checks_by_month.items():
        CandidateStats.add(
            month=checks_month,
            name=CandidateStatsName.CHECKS,
            count=checks_count,
        )

    logger.info("Calculating stats about listed candidates")
    CandidateStats.add(
        month=month,
        name=CandidateStatsName.LISTED_TOTAL,
        count=Candidate.count(),
    )
    CandidateStats.add(
        month=month,
        name=CandidateStatsName.LISTED_READY,
        count=Candidate.count_ready(),
    )
    CandidateStats.add(
        month=month,
        name=CandidateStatsName.LISTED_MEMBERS,
        count=Candidate.count_members(),
    )
    CandidateStats.add(
        month=month,
        name=CandidateStatsName.LISTED_FEMININE,
        count=Candidate.count_feminine(),
    )

    logger.info("Updating stats")
    with history_path.open("w") as f:
        for db_object in CandidateStats.history():
            f.write(db_object.serialize())


@cache(expire=timedelta(hours=1), ignore=(0,), tag="candidates-images")
@retry(
    retry=retry_if_exception_type(httpx.RequestError),
    wait=wait_random_exponential(max=60),
    stop=stop_after_attempt(3),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def download_image(client: httpx.AsyncClient, url: str) -> bytes:
    logger.debug(f"Downloading image: {url}")
    response = await client.get(url)
    response.raise_for_status()
    return response.content


def fetch_github_checks(
    api_key: str, *, pages_limit: int = 3, per_page: int = 100
) -> dict[str, int]:
    checks_by_month = defaultdict(int)
    page = 1
    with GitHub(api_key) as github:
        while page <= pages_limit:
            response = github.rest.issues.list_for_repo(
                owner="juniorguru",
                repo="eggtray",
                state="all",
                labels="check",
                sort="created",
                direction="desc",
                per_page=per_page,
                page=page,
            )
            issues = response.parsed_data
            if not issues:
                break
            for issue in issues:
                if getattr(issue, "pull_request", None):
                    continue
                checks_month = f"{issue.created_at:%Y-%m}"
                checks_by_month[checks_month] += 1
            if len(issues) < per_page:
                break
            page += 1
    return dict(checks_by_month)
