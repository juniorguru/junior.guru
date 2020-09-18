import hashlib
import logging
import time
from functools import wraps

from peewee import OperationalError

from juniorguru.models import Job
from juniorguru.models import db as default_db


logger = logging.getLogger(__name__)


def retry_when_db_locked(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        last_error = None
        for i in range(10):
            try:
                return method(self, *args, **kwargs)
            except OperationalError as error:
                if str(error) == 'database is locked':
                    logger.debug(f"Operation '{self.__class__.__name__}.{method.__name__}' failed! ({error}, attempt: {i + 1})")
                    last_error = error
                    time.sleep(0.5 * i)
                else:
                    raise
        raise last_error
    return wrapper


class Pipeline():
    def __init__(self, db=None, model=None, stats=None):
        self.db = db or default_db
        self.model = model or Job
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    @retry_when_db_locked
    def process_item(self, item, spider):
        with self.db:
            self.model.create(**prepare_data(item, spider.name))
        if self.stats:
            self.stats.inc_value('item_saved_count')
        return item


def prepare_data(item, spider_name):
    data = dict(**item, source=spider_name)
    if not data.get('id'):
        data['id'] = create_id(item)
    return data


def create_id(item):
    return hashlib.sha224('⚡︎'.join([
        item['link'],
        item['location'],
    ]).encode()).hexdigest()
