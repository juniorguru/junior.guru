import langdetect
from scrapy.exceptions import DropItem
from w3lib.html import remove_tags


class IrrelevantLanguage(DropItem):
    pass


class Pipeline():
    relevant_langs = ['cs', 'en']

    def process_item(self, item, spider):
        lang = langdetect.detect(remove_tags(item['description_raw']))
        if lang not in self.relevant_langs:
            raise IrrelevantLanguage(f"Language detected as '{lang}' (relevant: {', '.join(self.relevant_langs)})")
        item['lang'] = lang
        return item
