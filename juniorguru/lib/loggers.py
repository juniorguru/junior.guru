import logging
import os
from pathlib import Path
from typing import cast

from juniorguru.lib import global_state


MUTED_LOGGERS = [
    'discord',
    'peewee',
    'urllib3',
    'oauth2client',
    'google',
    'googleapiclient',
    'PIL',
    'asyncio',
    'MARKDOWN',
    'gql.transport.requests',
    'protego',
    'juniorguru.lib.discord_sync',
    'juniorguru.sync.club_content.store',
    'juniorguru.lib.mutations.allowing',
    'juniorguru.lib.discord_club.is_message_over_period_ago',
    'juniorguru.lib.discord_club.is_message_older_than',
    'juniorguru.web.templates',
]


class Logger(logging.Logger):
    def __getitem__(self, name) -> logging.Logger:
        return self.getChild(str(name))


def configure(level: str | None=None,
              format: str='[%(name)s] %(levelname)s: %(message)s',
              timestamp: bool | None=None):
    level = _get_level() if level is None else level.upper()
    timestamp = _get_timestamp() if timestamp is None else timestamp
    format = f'[%(asctime)s] {format}' if timestamp else format

    logging.setLoggerClass(Logger)
    logging.root.setLevel(logging.DEBUG)

    for name in MUTED_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    stderr = logging.StreamHandler()
    stderr.setLevel(getattr(logging, level))
    stderr.setFormatter(logging.Formatter(format))
    logging.root.addHandler(stderr)

    # In multiprocessing, the child processes won't automatically
    # inherit logger configuration and this function will run again.
    global_state.set('log_level', level)
    global_state.set('log_timestamp', 'true' if timestamp else 'false')


def _get_level() -> str:  # TODO test
    value = global_state.get('log_level')
    if value is None:
        value = os.getenv('LOG_LEVEL')
    if not value:
        return 'INFO'
    return value.upper()


def _get_timestamp() -> bool:  # TODO test
    value = global_state.get('log_timestamp')
    if value is None:
        value = os.getenv('LOG_TIMESTAMP')
    if value is None:
        value = os.getenv('CI')
    if not value or value.lower() in ['0', 'false']:
        return False
    return True


def get(name) -> Logger:
    return cast(Logger, logging.getLogger(name))


def from_path(path, cwd=None) -> Logger:
    cwd = cwd or os.getcwd()
    relative_path = str(Path(path).relative_to(cwd))
    name = '.'.join(
        relative_path
            .removesuffix('.py')
            .removesuffix('__init__')
            .rstrip('/')
            .split('/')
    )
    return get(name)


if not logging.root.hasHandlers():
    configure()
