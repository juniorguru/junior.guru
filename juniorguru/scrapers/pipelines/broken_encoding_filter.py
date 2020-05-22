from scrapy.exceptions import DropItem
from w3lib.html import remove_tags


class BrokenEncoding(DropItem):
    pass


class Pipeline():
    max_qm_count = 20

    def process_item(self, item, spider):
        qm_count = item['description_html'].count('?')
        print(qm_count)
        if qm_count <= self.max_qm_count:
            return item
        raise BrokenEncoding(f'Found {qm_count} question marks (limit: {self.max_qm_count})')
