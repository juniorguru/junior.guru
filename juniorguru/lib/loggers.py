import os
import logging


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
]


def configure():
    logging.root.setLevel(logging.DEBUG)

    for name in MUTED_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    stderr = logging.StreamHandler()
    stderr.setLevel(LOG_LEVEL)
    stderr.setFormatter(logging.Formatter('[%(name)s] %(levelname)s: %(message)s'))
    logging.root.addHandler(stderr)


def get(name):
    return logging.getLogger(name)


if not logging.root.hasHandlers():
    configure()
