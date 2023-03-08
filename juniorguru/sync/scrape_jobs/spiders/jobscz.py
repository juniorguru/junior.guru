import re

from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader

from juniorguru.lib.url_params import strip_params
from juniorguru.sync.scrape_jobs.items import Job, first, parse_relative_date, split


# TODO test board id parsing and params stripping
# https://www.jobs.cz/rpd/1615092148/?searchId=6c886dac-5152-476c-9e9e-211fe151ec68&rps=233
# https://www.jobs.cz/fp/eset-research-czech-republic-s-r-o-1702004793/1615818157/?positionOfAdInAgentEmail=0&searchId=6c886dac-5152-476c-9e9e-211fe151ec68&rps=233


class Spider(BaseSpider):
    name = 'jobscz'
    proxy = True
    download_timeout = 59
    download_delay = 1.25
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
    }

    start_urls = [
        'https://beta.www.jobs.cz/prace/?field%5B%5D=200900013&field%5B%5D=200900012&suitable-for=graduates',
    ]

    def parse(self, response):
        links = response.css('a[data-link="jd-detail"]::attr(href)').getall()
        yield from response.follow_all(links, callback=self.parse_job, cb_kwargs=dict(search_url=response.url))
        # TODO pagination?

    def parse_job(self, response, search_url):
        if 'www.jobs.cz' not in response.url:  # TODO custom job portals
            return
        loader = Loader(item=Job(), response=response)
        loader.add_value('source', self.name)
        loader.add_value('source_urls', search_url)
        loader.add_value('source_urls', response.url)
        loader.add_css('title', 'h1::text')
        loader.add_xpath('description_html', "//p[contains(text(), 'Úvodní představení')]/following-sibling::p")
        loader.add_css('description_html', '.content-rich-text')
        # loader.add_css('remote', 'h2::text') TODO
        loader.add_value('url', response.url)
        loader.add_xpath('company_name', "//dt[contains(text(), 'Společnost')]/following-sibling::dd/text()")
        item = loader.load_item()
        yield item


def parse_remote(text):  # TODO
    return bool(re.search(r'\bremote\b', text, re.IGNORECASE))


def clean_url(url):
    return strip_params(url, ['positionOfAdInAgentEmail', 'searchId', 'rps'])


def join(values):
    return ''.join(values)


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    url_in = Compose(first, clean_url)
    company_url_in = Compose(first, clean_url)
    employment_types_in = MapCompose(str.lower, split)
    employment_types_out = Identity()
    first_seen_on_in = Compose(first, parse_relative_date)
    description_html_out = Compose(join)
    experience_levels_in = MapCompose(str.lower, split)
    experience_levels_out = Identity()
    company_logo_urls_out = Identity()
    # remote_in = MapCompose(parse_remote) TODO
    locations_raw_out = Identity()
