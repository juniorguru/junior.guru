import logging
from pathlib import Path
import os


LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'info').upper())
LOG_FILE = Path(__file__).parent.parent / 'data' / 'sync.log'


formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')

stderr_handler = logging.StreamHandler()
stderr_handler.setLevel(LOG_LEVEL)
stderr_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename=LOG_FILE, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


def get(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(stderr_handler)
    log.addHandler(file_handler)
    return log
