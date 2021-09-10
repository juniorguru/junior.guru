import langdetect
from w3lib.html import remove_tags


class Pipeline():
    def process_item(self, item, spider):
        item['lang'] = langdetect.detect(remove_tags(item['description_html']))
        return item
