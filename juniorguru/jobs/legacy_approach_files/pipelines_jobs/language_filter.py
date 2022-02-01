from scrapy.exceptions import DropItem


class IrrelevantLanguage(DropItem):
    pass


class Pipeline():
    relevant_langs = ['cs', 'en']

    def process_item(self, item, spider):
        if item['lang'] not in self.relevant_langs:
            raise IrrelevantLanguage(f"Language detected as '{item['lang']}' (relevant: {', '.join(self.relevant_langs)})")
        return item
