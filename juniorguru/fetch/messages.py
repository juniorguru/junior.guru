import re
import os

import discord

from juniorguru.lib.log import get_log


log = get_log('messages')


JUNIORGURU_GUILD_NUM = 769966886598737931
EXCLUDE_CATEGORIES = ['coreskill']
KEYWORDS = {re.compile(r'\b' + key + r'\b', re.IGNORECASE): value for key, value in {
    r'pyladies': 'pyladies',
    r'coursera': 'coursera',
    r'codea?cademy': 'codecademy',
    r'edx': 'edx',
    r'pluralsight': 'pluralsight',
    r'udacity': 'udacity',
    r'udemy': 'udemy',
    r'egghead': 'egghead',
    r'engeto': 'engeto',
    r'czechitas': 'czechitas',
    r'green ?fox': 'greenfox',
    r'codingbootcamp\.cz': 'codingbootcamppraha',
    r'coding ?boo?tcamp pra(ha|gue)': 'codingbootcamppraha',
    r'data4you': 'codingbootcamppraha',
    r'core ?skill': 'coreskill',
    r'kurzy\.vsb': 'vsb',
    r'všb': 'vsb',
    r'it[ \-]?network': 'itnetwork',
    r'femm?e ?pall?ett?e': 'femmepalette',
    r'react ?girls': 'reactgirls',
    r'django ?girls': 'djangogirls',
    r'rails ?girls': 'railsgirls',
    r'č\.d\.?': 'ceskodigital',
    r'česko\.?digit[aá]l': 'ceskodigital',
    r'beeit': 'beeit',
}.items()}
IS_RELEVANT_RE = re.compile('|'.join([keyword.pattern for keyword in KEYWORDS.keys()]), re.IGNORECASE)


async def run(client):
    for channel in client.get_guild(JUNIORGURU_GUILD_NUM).text_channels:
        if channel.category and channel.category.name.lower() in EXCLUDE_CATEGORIES:
            continue
        async for message in channel.history(limit=None, after=None).filter(is_relevant):
            print(repr(channel.name),
                  repr(sum([reaction.count for reaction in message.reactions])),
                  repr(message.content))


def is_relevant(message):
    return bool(IS_RELEVANT_RE.search(message.content))


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
