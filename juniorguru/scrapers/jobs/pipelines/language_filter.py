from scrapy.exceptions import DropItem


class IrrelevantLanguage(DropItem):
    pass


class Pipeline():
    RELEVANT_LANGS = ['cs', 'en']

    def process_item(self, item, spider):
        if item['lang'] not in self.RELEVANT_LANGS:
            raise IrrelevantLanguage(f"Language detected as '{item['lang']}' (relevant: {', '.join(self.RELEVANT_LANGS)})")
        return item
