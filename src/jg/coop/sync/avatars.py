import asyncio
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.chunks import chunks
from jg.coop.lib.discord_club import ClubClient
from jg.coop.models.base import db
from jg.coop.models.club import ClubUser


logger = loggers.from_path(__file__)


IMAGES_PATH = Path("src/jg/coop/images")

AVATARS_PATH = IMAGES_PATH / "avatars-club"

MEMBERS_CHUNK_SIZE = 10

AVATARS_LIMIT = 40

AVATAR_SIZE_PX = 120


@cli.sync_command(dependencies=["club-content"])
def main():
    discord_task.run(fetch_avatars)


@db.connection_context()
async def fetch_avatars(client: ClubClient):
    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob("*.png"):
        path.unlink()

    members_chunks = chunks(
        ClubUser.members_listing(shuffle=True), size=MEMBERS_CHUNK_SIZE
    )
    for n, members_chunk in enumerate(members_chunks, start=1):
        logger.debug(f"Processing chunk #{n} of {len(members_chunk)} members")
        await asyncio.gather(
            *[process_member(client, member) for member in members_chunk]
        )

        avatars_count = ClubUser.avatars_count()
        logger.debug(
            f"There are total {avatars_count} avatars after processing the chunk #{n}"
        )
        if avatars_count >= AVATARS_LIMIT:
            logger.debug(f"Done! Got {avatars_count} avatars, need {AVATARS_LIMIT}")
            break


async def process_member(client: ClubClient, member):
    logger_m = logger[str(member.id)]
    logger_m.info(f"Checking avatar of #{member.id}")
    try:
        discord_member = await client.club_guild.fetch_member(member.id)
        avatar = discord_member.display_avatar
        if avatar and not is_default_avatar(avatar.url):
            logger_m.info(f"Has avatar, downloading {avatar.url}")
            member.avatar_path = await download_avatar(avatar)
        if member.avatar_path:
            logger_m.info(f"Has avatar, downloaded as '{member.avatar_path}'")
        else:
            logger_m.info("Has no avatar")
    except Exception:
        logger_m.exception("Unable to get avatar")
    member.save()


async def download_avatar(avatar) -> str:
    buffer = BytesIO()
    await avatar.save(buffer)
    image = Image.open(buffer)
    image = image.resize((AVATAR_SIZE_PX, AVATAR_SIZE_PX))
    image_path = AVATARS_PATH / f"{Path(urlparse(avatar.url).path).stem}.png"
    image.save(image_path, "PNG")
    return f"avatars-club/{image_path.name}"


def is_default_avatar(url: str) -> bool:
    return "/embed/avatars/" in url
