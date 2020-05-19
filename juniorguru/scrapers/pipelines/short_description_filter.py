from scrapy.exceptions import DropItem
from w3lib.html import remove_tags


class ShortDescription(DropItem):
    pass


class Pipeline():
    min_chars_count = 600

    def process_item(self, item, spider):
        chars_count = len(remove_tags(item['description_html']))
        if chars_count >= self.min_chars_count:
            return item
        raise ShortDescription(f'Description is only {chars_count} characters (limit: {self.min_chars_count})')
