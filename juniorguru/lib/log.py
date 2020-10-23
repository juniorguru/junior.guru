import logging
import os


LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'info').upper())


logging.basicConfig(format='[%(name)s] %(levelname)s: %(message)s',
                    level=LOG_LEVEL)


def get_log(name):
    return logging.getLogger(name)
