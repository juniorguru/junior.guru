import asyncio
import os
import threading
from typing import Awaitable, Callable

from jg.coop.lib import loggers
from jg.coop.lib.discord_club import ClubClient


DISCORD_API_KEY = os.getenv("DISCORD_API_KEY") or None


logger = loggers.from_path(__file__)


def run(task_fn: Callable[..., Awaitable], *args, **kwargs) -> None:
    """
    Run given async function in a separate process.

    Separate process is used so that it's possible to run multiple one-time
    async tasks independently on each other, in separate async loops.
    """
    exc = None

    def _discord_thread(task_fn: Callable[..., Awaitable], args, kwargs) -> None:
        if not asyncio.iscoroutinefunction(task_fn):
            raise TypeError(
                f"Not async function: {task_fn.__qualname__} from {task_fn.__module__}"
            )

        class Client(ClubClient):
            async def on_ready(self):
                await self.wait_until_ready()
                logger.debug("Discord connection ready")
                await task_fn(self, *args, **kwargs)
                logger.debug("Closing Discord client")
                await self.close()

            async def on_error(self, event, *args, **kwargs):
                logger.debug("Got an error, raising")
                raise

        client = Client(loop=asyncio.new_event_loop())

        def exc_handler(loop, context):
            nonlocal exc
            exc = context.get("exception")
            logger.debug(f"Recording exception: {exc}")
            loop.default_exception_handler(context)
            logger.debug("Stopping async execution")
            loop.stop()

        client.loop.set_exception_handler(exc_handler)
        logger.debug("Starting")
        client.run(DISCORD_API_KEY)

    thread = threading.Thread(target=_discord_thread, args=[task_fn, args, kwargs])
    thread.start()
    thread.join()

    if exc:
        logger.debug("Found exception, raising")
        raise exc
