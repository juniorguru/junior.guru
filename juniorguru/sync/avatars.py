from pathlib import Path
from urllib.parse import urlparse
from io import BytesIO

from PIL import Image

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, is_default_avatar
from juniorguru.models import ClubUser, db


logger = loggers.get('avatars')


IMAGES_PATH = Path(__file__).parent.parent / 'images'
AVATARS_PATH = IMAGES_PATH / 'avatars'
AVATAR_SIZE_PX = 60


@measure('avatars')
@discord_task
async def main(client):
    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob('*.png'):
        path.unlink()

    with db:
        for member in ClubUser.members_listing():
            logger.info(f"Downloading avatar for '{member.display_name}' #{member.id}")
            discord_member = await client.juniorguru_guild.fetch_member(member.id)
            member.avatar_path = await download_avatar(discord_member)
            logger.info(f"Result: '{member.avatar_path}'")
            member.save()


async def download_avatar(discord_member):
    avatar_url = str(discord_member.avatar_url)
    if is_default_avatar(avatar_url):
        return None
    else:
        buffer = BytesIO()
        await discord_member.avatar_url.save(buffer)
        image = Image.open(buffer)
        image = image.resize((AVATAR_SIZE_PX, AVATAR_SIZE_PX))
        image_path = AVATARS_PATH / f'{Path(urlparse(avatar_url).path).stem}.png'
        image.save(image_path, 'PNG')
        return f'images/avatars/{image_path.name}'


if __name__ == '__main__':
    main()
