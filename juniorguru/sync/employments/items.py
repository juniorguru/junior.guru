from scrapy import Field, Item


class Employment(Item):
    id = Field()
    title = Field()
    company_name = Field()
    url = Field()
    apply_url = Field()
    external_ids = Field()
    locations = Field()
    lang = Field()
    description_html = Field()
    seen_at = Field()
    source = Field()
    source_urls = Field()
    adapter = Field()
    build_url = Field()
