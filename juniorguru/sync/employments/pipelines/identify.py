import hashlib

from scrapy.exceptions import DropItem


class MissingIdentifierField(DropItem):
    pass


class Pipeline():
    def process_item(self, item, spider):
        if not item.get('id'):
            try:
                item['id'] = create_id(item)
            except KeyError as exc:
                raise MissingIdentifierField(str(exc))
        return item


def create_id(item):
    return hashlib.sha224(item['url'].encode()).hexdigest()
