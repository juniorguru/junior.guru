import logging
import os
from pathlib import Path
from typing import cast

from juniorguru.lib import global_state


LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'info').upper())

LOG_FORMAT = '[%(name)s] %(levelname)s: %(message)s'

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
    'juniorguru.lib.discord_club.is_message_over_period_ago',
    'juniorguru.lib.discord_club.is_message_older_than',
    'juniorguru.lib.images',
    'juniorguru.mkdocs.templates',
]


class Logger(logging.Logger):
    def __getitem__(self, name) -> logging.Logger:
        return self.getChild(str(name))


def configure():
    logging.setLoggerClass(Logger)
    logging.root.setLevel(logging.DEBUG)

    for name in MUTED_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    stderr = logging.StreamHandler()
    stderr.setLevel(LOG_LEVEL)
    stderr.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.root.addHandler(stderr)

    # In multiprocessing, the child processes won't automatically
    # inherit logger configuration and this function will run again.
    # If there's already a log path set in the global state,
    # let's configue it for this process too.
    log_path = global_state.get('loggers.log_path')
    if log_path:
        configure_file(log_path)


def configure_file(path):
    global_state.set('loggers.log_path', str(path))
    file = logging.FileHandler(path, mode='w')
    file.setLevel(logging.DEBUG)
    file.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.root.addHandler(file)


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
