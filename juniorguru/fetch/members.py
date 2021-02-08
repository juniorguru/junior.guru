import re
import os
from urllib.parse import urlparse
from pathlib import Path
from io import BytesIO

import discord
from PIL import Image

from juniorguru.lib.log import get_log
from juniorguru.models import Member, db


log = get_log('members')


JUNIORGURU_GUILD_NUM = 769966886598737931
IMAGES_PATH = Path(__file__).parent.parent / 'data' / 'images'
AVATARS_PATH = IMAGES_PATH / 'avatars'
SIZE_PX = 60


async def run(client):
    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob('*'):
        path.unlink()

    with db:
        Member.drop_table()
        Member.create_table()

    async for member in client.get_guild(JUNIORGURU_GUILD_NUM).fetch_members(limit=None):
        if not member.bot:
            id = member.id
            log.info(f'Member {id}')
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
            Member.create(id=id, avatar_path=avatar_path)


def is_default_avatar(url):
    return bool(re.search(r'/embed/avatars/\d+\.', url))



def main():
    class Client(discord.Client):
        async def on_ready(self):
            await self.wait_until_ready()
            await run(self)
            await self.close()

        async def on_error(self, event, *args, **kwargs):
            raise

    # oauth permissions: manage guild
    intents = discord.Intents(guilds=True, members=True)
    client = Client(intents=intents)

    exc = None
    def exc_handler(loop, context):
        nonlocal exc
        exc = context.get('exception')
        loop.default_exception_handler(context)
        loop.stop()

    client.loop.set_exception_handler(exc_handler)
    client.run(os.environ['DISCORD_API_KEY'])

    if exc:
        raise exc


if __name__ == '__main__':
    main()
