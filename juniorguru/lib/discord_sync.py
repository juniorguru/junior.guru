import asyncio

import discord


def run(fn, api_key, intents=None):
    class Client(discord.Client):
        async def on_ready(self):
            await self.wait_until_ready()
            await fn(self)
            await self.close()

        async def on_error(self, event, *args, **kwargs):
            raise

    intents = discord.Intents(**{intent: True for intent in (intents or {})})
    client = Client(loop=asyncio.new_event_loop(), intents=intents)

    exc = None
    def exc_handler(loop, context):
        nonlocal exc
        exc = context.get('exception')
        loop.default_exception_handler(context)
        loop.stop()

    client.loop.set_exception_handler(exc_handler)
    client.run(api_key)

    if exc:
        raise exc
