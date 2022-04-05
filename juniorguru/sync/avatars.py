from pathlib import Path
from urllib.parse import urlparse
from io import BytesIO
import asyncio

from PIL import Image

from juniorguru.lib.tasks import sync_task
from juniorguru.sync.club_content import main as club_content_task
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task
from juniorguru.models import ClubUser, db


logger = loggers.get(__name__)


IMAGES_PATH = Path(__file__).parent.parent / 'images'

AVATARS_PATH = IMAGES_PATH / 'avatars'

MEMBERS_CHUNK_SIZE = 10

AVATARS_LIMIT = 40

AVATAR_SIZE_PX = 60


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.avatars.discord_task')


@db.connection_context()
async def discord_task(client):
    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob('*.png'):
        path.unlink()

    members_chunks = chunks(ClubUser.members_listing(shuffle=True),
                            size=MEMBERS_CHUNK_SIZE)
    for n, members_chunk in enumerate(members_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(members_chunk)} members')
        await asyncio.gather(*[
            process_member(client, member)
            for member in members_chunk
        ])

        avatars_count = ClubUser.avatars_count()
        logger.debug(f'There are total {avatars_count} avatars after processing the chunk #{n}')
        if avatars_count >= AVATARS_LIMIT:
            logger.debug(f"Done! Got {avatars_count} avatars, need {AVATARS_LIMIT}")
            break


def chunks(iterable, size=1):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


async def process_member(client, member):
    logger_m = logger.getChild(str(member.id))
    logger_m.info('Checking avatar')
    logger_m.debug(f"Name: {member.display_name}")
    try:
        discord_member = await client.juniorguru_guild.fetch_member(member.id)
        if discord_member.avatar:
            logger_m.info("Has avatar, downloading")
            member.avatar_path = await download_avatar(discord_member.avatar)
        if member.avatar_path:
            logger_m.info(f"Has avatar, downloaded as '{member.avatar_path}'")
        else:
            logger_m.info("Has no avatar")
    except:
        logger_m.exception("Unable to get avatar")
    member.save()


async def download_avatar(avatar):
    buffer = BytesIO()
    await avatar.save(buffer)
    image = Image.open(buffer)
    image = image.resize((AVATAR_SIZE_PX, AVATAR_SIZE_PX))
    image_path = AVATARS_PATH / f'{Path(urlparse(avatar.url).path).stem}.png'
    image.save(image_path, 'PNG')
    return f'images/avatars/{image_path.name}'
