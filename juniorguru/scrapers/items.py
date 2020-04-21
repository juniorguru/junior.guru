from scrapy import Item, Field


class Job(Item):
    title = Field()
    link = Field()
    company_name = Field()
    company_link = Field()
    location_raw = Field()
    employment_types = Field()
    timestamp = Field()
    description_raw = Field()
