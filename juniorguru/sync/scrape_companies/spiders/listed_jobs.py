from pathlib import Path

from scrapy import Spider as BaseSpider

from juniorguru.sync.scrape_companies.items import Company
from juniorguru.models import db, ListedJob


# TODO chceme stahnout nejaky obrazek a to muzeme bud z urls ktery sou ulozeny
# v db ke kazdymu jobu, nebo se snazime najit nakej favicon?


class Spider(BaseSpider):
    name = 'listed_jobs'

    # Working around the fact that Scrapy spiders must start with
    # at least one request. Scraping this file from local filesystem
    # and dropping the response (see second argument of the 'parse'
    # method).
    #
    # In the future, if it makes sense to actually perform a request
    # per company, solution may look like https://stackoverflow.com/a/46339560/325365
    # or the Scrapy's start_requests() method can be used.
    start_urls = [f'file://{Path(__file__).absolute()}']
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse(self, _):
        with db.connection_context():
            for job in ListedJob.listing():
                yield Company(name=job.company_name,
                              url=job.company_url,
                              logo_urls=job.company_logo_urls)
