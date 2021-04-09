import hashlib


class Pipeline():
    def process_item(self, item, spider):
        if not item.get('id'):
            item['id'] = create_id(item)
        return item


def create_id(item):
    return hashlib.sha224(item['link'].encode()).hexdigest()
