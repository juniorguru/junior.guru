from scrapy import Field, Item


class Employment(Item):
    id = Field()
    title = Field()
    company_name = Field()
    url = Field()
    description_html = Field()
    seen_at = Field()
    source = Field()
    source_url = Field()
