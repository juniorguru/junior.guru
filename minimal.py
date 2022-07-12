import os

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # my server
    guild = client.get_guild(769966886598737931)

    # problematic thread (but hundreds of others work just fine,
    # also 2.0.0-rc.1 works just fine)
    thread = await guild.fetch_channel(923161263243165757)
    print(repr(thread), repr(thread.guild))

    # the following line raises
    #
    #   ...
    #   File "/Users/honza/Library/Caches/pypoetry/virtualenvs/juniorguru-Lgaxwd2n-py3.8/lib/python3.8/site-packages/discord/threads.py", line 191, in _from_data
    #     if thread := self.guild.get_thread(self.id) and data.pop("_invoke_flag", False):
    # AttributeError: 'NoneType' object has no attribute 'get_thread'
    async for message in thread.history():
        pass


client.run(os.getenv('DISCORD_API_KEY'))
