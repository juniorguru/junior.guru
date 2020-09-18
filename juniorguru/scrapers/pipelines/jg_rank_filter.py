from scrapy.exceptions import DropItem


class NotEntryLevel(DropItem):
    pass


class Pipeline():
    min_jg_rank = 1

    def process_item(self, item, spider):
        if item['jg_rank'] < self.min_jg_rank:
            raise NotEntryLevel(f"JG rank is {item['jg_rank']} (minimum: {self.min_jg_rank})")
        return item
