import asyncio
import os
import sys
import threading
from queue import Queue
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
    exc_queue = Queue()

    def _discord_thread(task_fn: Callable[..., Awaitable], args, kwargs) -> None:
        if not asyncio.iscoroutinefunction(task_fn):
            exc = TypeError(
                f"Not async function: {task_fn.__qualname__} from {task_fn.__module__}"
            )
            exc_queue.put(exc)

        class Client(ClubClient):
            async def on_ready(self):
                await self.wait_until_ready()
                logger.debug("Discord connection ready")
                try:
                    await task_fn(self, *args, **kwargs)
                except Exception as exc:
                    logger.debug("Task function raised an exception")
                    exc_queue.put(exc)
                finally:
                    logger.debug("Closing Discord client")
                    await self.close()

            async def on_error(self, event, *args, **kwargs):
                logger.debug("Got an error")
                exc_type, exc_value, tb = sys.exc_info()
                exc_queue.put(exc_value)

        logger.debug("Starting")
        try:
            client = Client(loop=asyncio.new_event_loop())
            client.run(DISCORD_API_KEY)
        except Exception as exc:
            logger.debug("Discord client raised an exception")
            exc_queue.put(exc)

    thread = threading.Thread(target=_discord_thread, args=[task_fn, args, kwargs])
    thread.start()
    thread.join()

    if not exc_queue.empty():
        raise exc_queue.get()
