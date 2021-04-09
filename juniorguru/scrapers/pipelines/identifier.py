import hashlib

from scrapy.exceptions import DropItem


class MissingIdentifyingField(DropItem):
    pass


class Pipeline():
    def process_item(self, item, spider):
        if not item.get('id'):
            try:
                item['id'] = create_id(item)
            except KeyError as exc:
                raise MissingIdentifyingField(str(exc))
        return item


def create_id(item):
    return hashlib.sha224(item['link'].encode()).hexdigest()
