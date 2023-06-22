import logging
import os
from pathlib import Path
from typing import cast


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
              timestamp: bool=False):
    level = getattr(logging, (level or 'INFO').upper())
    format = f'[%(asctime)s] {format}' if timestamp else format

    logging.setLoggerClass(Logger)
    logging.root.setLevel(logging.DEBUG)

    for name in MUTED_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    stderr = logging.StreamHandler()
    stderr.setLevel(level)
    stderr.setFormatter(logging.Formatter(format))
    logging.root.addHandler(stderr)


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


def level_from_env(env: dict) -> str:  # TODO test
    value = env.get('LOG_LEVEL')
    if not value:
        return None
    return value.upper()


def timestamp_from_env(env: dict) -> bool:  # TODO test
    value = env.get('LOG_TIMESTAMP')
    if value is None:
        value = env.get('CI')
    if not value or value.lower() in ['0', 'false']:
        return False
    return True


if not logging.root.hasHandlers():
    configure(level=level_from_env(os.environ),
              timestamp=timestamp_from_env(os.environ))
