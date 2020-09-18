import hashlib

from juniorguru.models import Job
from juniorguru.models import db as default_db


class Pipeline():
    def __init__(self, db=None, model=None, stats=None):
        self.db = db or default_db
        self.model = model or Job
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_item(self, item, spider):
        with self.db:
            self.model.create(**prepare_job_data(item, spider.name))
        if self.stats:
            self.stats.inc_value('item_saved_count')
        return item


def item_to_job_id(item):
    return hashlib.sha224('⚡︎'.join([
        item['link'],
        item['location'],
    ]).encode()).hexdigest()


def prepare_job_data(item, spider_name):
    data = dict(**item, source=spider_name)
    data.setdefault('id', item_to_job_id(item))
    return data
