from scrapy.exceptions import DropItem


class NotEntryLevel(DropItem):
    pass


class Pipeline():
    min_junior_rank = 1

    def process_item(self, item, spider):
        if item['junior_rank'] < self.min_junior_rank:
            raise NotEntryLevel(f"Junior rank is {item['junior_rank']} (minimum: {self.min_junior_rank})")
        return item
