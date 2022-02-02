from scrapy.exceptions import DropItem


class BrokenEncoding(DropItem):
    pass


class Pipeline():
    MAX_QM_COUNT = 20

    def process_item(self, item, spider):
        qm_count = item['description_html'].count('?')
        if qm_count <= self.MAX_QM_COUNT:
            return item
        raise BrokenEncoding(f'Found {qm_count} question marks (limit: {self.MAX_QM_COUNT})')
