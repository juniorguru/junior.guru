import re
from urllib.parse import urlparse
from pathlib import Path
from io import BytesIO

from PIL import Image

from juniorguru.lib.log import get_log
from juniorguru.lib import club
from juniorguru.models import Member, db


log = get_log('members')


IMAGES_PATH = Path(__file__).parent.parent / 'data' / 'images'
AVATARS_PATH = IMAGES_PATH / 'avatars'
SIZE_PX = 60


@club.discord_task
async def main(client):
    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob('*'):
        path.unlink()

    with db:
        Member.drop_table()
        Member.create_table()

    async for member in client.juniorguru_guild.fetch_members(limit=None):
        if not member.bot:
            log.debug(f'Member {member.display_name} {member.id}')
            avatar_url = str(member.avatar_url)
            if is_default_avatar(avatar_url):
                avatar_path = None
            else:
                buffer = BytesIO()
                await member.avatar_url.save(buffer)
                image = Image.open(buffer)
                image = image.resize((SIZE_PX, SIZE_PX))
                image_path = AVATARS_PATH / f'{Path(urlparse(avatar_url).path).stem}.png'
                image.save(image_path, 'PNG')
                avatar_path = f'images/avatars/{image_path.name}'
            Member.create(id=member.id, avatar_path=avatar_path)

        # if member.display_name == 'DanielSrb':
        #     if not member.dm_channel:
        #         await member.create_dm()
        #     await member.dm_channel.send(content='Ahoj Dane, mám tě rád ❤️')


def is_default_avatar(url):
    return bool(re.search(r'/embed/avatars/\d+\.', url))


if __name__ == '__main__':
    main()
