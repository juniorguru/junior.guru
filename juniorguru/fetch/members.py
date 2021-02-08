import re
import os

import discord

from juniorguru.lib.log import get_log
from juniorguru.models import Member, db


log = get_log('members')


JUNIORGURU_GUILD_NUM = 769966886598737931


async def run(client):
    with db:
        Member.drop_table()
        Member.create_table()

    async for member_data in client.get_guild(JUNIORGURU_GUILD_NUM).fetch_members(limit=None):
        if not member_data.bot:
            id = member_data.id
            log.info(f'Member {id}')
            avatar_url = str(member_data.avatar_url)
            Member.create(id=id,
                          avatar_url=None if is_default_avatar(avatar_url) else avatar_url)


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
