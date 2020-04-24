from scrapy import Item, Field


class Job(Item):
    posted_at = Field()
    title = Field()
    location = Field()
    company_name = Field()
    company_link = Field()
    employment_types = Field()
    description_raw = Field()
    lang = Field()
    link = Field()


def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)
