from juniorguru.models import Job, retry_when_db_locked, db as default_db


class Pipeline():
    def __init__(self, db=None, model=None, stats=None):
        self.db = db or default_db
        self.model = model or Job
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_item(self, item, spider):
        def operation():
            data = dict(**item, source=spider.name)
            self.model.create(**data)
            if self.stats:
                self.stats.inc_value('item_saved_count')
            return item
        return retry_when_db_locked(self.db, operation, stats=self.stats)
