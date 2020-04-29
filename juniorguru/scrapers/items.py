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
    experience_levels = Field()


def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)


def split(string, by=','):
    if string:
        return list(filter(None, map(str.strip, string.split(by))))
    return []
