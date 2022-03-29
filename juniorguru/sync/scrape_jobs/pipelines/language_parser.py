import langdetect
from w3lib.html import remove_tags


class Pipeline():
    def process_item(self, item, spider):
        item['lang'] = parse(item['description_html'])
        return item


def parse(description_html):
    return langdetect.detect(remove_tags(description_html))
