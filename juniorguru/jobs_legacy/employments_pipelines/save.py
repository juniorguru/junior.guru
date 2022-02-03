from juniorguru.models import Employment, retry_when_db_locked, db as default_db


class Pipeline():
    def __init__(self, db=None, model=None, stats=None):
        self.db = db or default_db
        self.model = model or Employment
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats)

    def process_item(self, item, spider):
        def operation():
            try:
                stats_value = 'item_merged_count'
                employment = self.model.get_by_item(item)
                employment.merge_item(item)
                employment.save()
            except self.model.DoesNotExist:
                stats_value = 'item_saved_count'
                employment = self.model.from_item(item)
                employment.save(force_insert=True)
            if self.stats:
                self.stats.inc_value(stats_value)
            return item
        return retry_when_db_locked(self.db, operation, stats=self.stats)
