from scrapy import Field, Item

from juniorguru.lib.repr import repr_item


class Company(Item):
    name = Field()
    url = Field()
    logo_urls = Field()
    logos = Field()
    logo_path = Field()

    def __repr__(self):
        return repr_item(self, ['name', 'url'])
