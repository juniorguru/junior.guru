import hashlib

from .. import models


class Database():
    def __init__(self, db=None, job_cls=None, stats=None):
        self.db = db or models.db
        self.job_cls = job_cls or models.Job
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def open_spider(self, spider):
        self.db.connect()

    def process_item(self, item, spider):
        self.job_cls.create(**prepare_job_data(item, spider.name))
        if self.stats:
            self.stats.inc_value('item_saved_count')
        return item

    def close_spider(self, spider):
        self.db.close()


def prepare_job_data(item, spider_name):
    return dict(
        **item,
        id=hashlib.sha224(item['link'].encode()).hexdigest(),
        source=spider_name,
        # is_approved=True,
    )
