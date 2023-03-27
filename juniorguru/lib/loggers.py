import logging
import os
from pathlib import Path


LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'info').upper())

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
    'juniorguru.lib.club.is_message_over_period_ago',
    'juniorguru.lib.club.is_message_older_than',
    'juniorguru.lib.images',
    'juniorguru.mkdocs.templates',
]


class Logger(logging.Logger):
    def __getitem__(self, name) -> logging.Logger:
        return self.getChild(name)


def configure():
    logging.setLoggerClass(Logger)
    logging.root.setLevel(logging.DEBUG)

    for name in MUTED_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    stderr = logging.StreamHandler()
    stderr.setLevel(LOG_LEVEL)
    stderr.setFormatter(logging.Formatter('[%(name)s] %(levelname)s: %(message)s'))
    logging.root.addHandler(stderr)


def get(name) -> logging.Logger:
    return logging.getLogger(name)


def from_path(path, cwd=None) -> logging.Logger:
    cwd = cwd or os.getcwd()
    relative_path = str(Path(path).relative_to(cwd))
    name = '.'.join(relative_path.removesuffix('.py').removesuffix('__init__').split('/'))
    return get(name)


if not logging.root.hasHandlers():
    configure()
