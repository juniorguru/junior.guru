import asyncio
import importlib
import os
from multiprocessing import Process

from juniorguru.lib import loggers
from juniorguru.lib.discord_club import ClubClient
from juniorguru.lib.mutations import mutations


DISCORD_API_KEY = os.getenv('DISCORD_API_KEY') or None


logger = loggers.from_path(__file__)


def run(fn, *args):
    """
    Run given async function in a separate process.

    Separate process is used so that it's possible to run multiple one-time
    async tasks independently on each other, in separate async loops.
    """
    import_path = get_import_path(fn)
    logger.debug(f'Running async code in a separate process: {import_path}')
    process = Process(target=discord_process, args=[import_path, mutations.dump(), args])
    process.start()
    process.join()
    if process.exitcode != 0:
        raise RuntimeError(f'Process for running async code finished with non-zero exit code: {process.exitcode}')


def get_import_path(fn):
    return f'{fn.__module__}.{fn.__qualname__}'


def discord_process(import_path, mutations_dump, args):
    mutations.load(mutations_dump)
    logger_dt = logger['discord_task']

    import_path_parts = import_path.split('.')
    module = importlib.import_module('.'.join(import_path_parts[:-1]))
    task_fn = getattr(module, import_path_parts[-1])
    logger_dt.debug(f'Imported {task_fn.__qualname__} from {task_fn.__module__}')

    if not asyncio.iscoroutinefunction(task_fn):
        raise TypeError(f"Not async function: {task_fn.__qualname__} from {task_fn.__module__}")

    class Client(ClubClient):
        async def on_ready(self):
            await self.wait_until_ready()
            logger_dt.debug('Discord connection ready')
            await task_fn(self, *args)
            logger_dt.debug('Closing Discord client')
            await self.close()

        async def on_error(self, event, *args, **kwargs):
            logger_dt.debug('Got an error, raising')
            raise

    client = Client()

    exc = None
    def exc_handler(loop, context):
        nonlocal exc
        logger_dt.debug('Recording exception')
        exc = context.get('exception')
        loop.default_exception_handler(context)
        logger_dt.debug('Stopping async execution')
        loop.stop()

    client.loop.set_exception_handler(exc_handler)
    logger_dt.debug('Starting')
    client.run(DISCORD_API_KEY)

    if exc:
        logger_dt.debug('Found exception, raising')
        raise exc
