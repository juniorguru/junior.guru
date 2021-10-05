import logging
from pathlib import Path
import os


LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'info').upper())
LOG_FILE = Path(__file__).parent.parent / 'data' / 'sync.log'


def configure():
    logging.root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')

    stderr = logging.StreamHandler()
    stderr.setLevel(LOG_LEVEL)
    stderr.setFormatter(formatter)
    logging.root.addHandler(stderr)

    file = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
    file.setLevel(logging.DEBUG)
    file.setFormatter(formatter)
    logging.root.addHandler(file)


def get(name):
    return logging.getLogger(name)


if not logging.root.hasHandlers():
    configure()
