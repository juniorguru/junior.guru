import os

import discord

from juniorguru.lib.log import get_log


log = get_log('club_members')


async def run(client):
    # channel = client.get_channel(797107515186741248)
    # await channel.send(client.user.name)
    from pprint import pprint
    guild = client.get_guild(769966886598737931)
    print('MEMBERS')
    pprint(guild.members)
    print('INVITES')
    pprint(await guild.invites())


def main():
    class Client(discord.Client):
        async def on_ready(self):
            await self.wait_until_ready()
            await run(self)
            await self.close()

        async def on_error(self, event, *args, **kwargs):
            raise

    # oauth permissions: manage guild, create invites
    intents = discord.Intents(guilds=True, members=True, messages=True, invites=True)
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
