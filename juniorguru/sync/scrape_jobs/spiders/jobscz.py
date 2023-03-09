from datetime import date

from itemloaders.processors import Compose, Identity, TakeFirst
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader

from juniorguru.lib import loggers
from juniorguru.lib.url_params import strip_params
from juniorguru.sync.scrape_jobs.items import Job, first


logger = loggers.from_path(__file__)


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
        logger.warning('Not implemented yet: pagination')

    def parse_job(self, response, search_url):
        if 'www.jobs.cz' not in response.url:
            logger.warning('Not implemented yet: custom job portals')
            return
        loader = Loader(item=Job(), response=response)
        loader.add_value('source', self.name)
        loader.add_value('source_urls', search_url)
        loader.add_value('source_urls', response.url)
        loader.add_value('first_seen_on', date.today())
        loader.add_css('title', 'h1::text')
        loader.add_xpath('company_name', "//span[contains(text(), 'Společnost')]/following-sibling::p/text()")
        loader.add_css('locations_raw', 'a[href*="mapy.cz"]::text')
        loader.add_xpath('employment_types', "//span[contains(text(), 'Typ pracovního poměru')]/following-sibling::p/text()")
        loader.add_xpath('description_html', "//p[contains(text(), 'Úvodní představení')]/following-sibling::p")
        loader.add_css('description_html', '.content-rich-text')
        loader.add_value('url', response.url)
        item = loader.load_item()
        yield item


def clean_url(url):
    return strip_params(url, ['positionOfAdInAgentEmail', 'searchId', 'rps'])


def join(values):
    return ''.join(values)


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    url_in = Compose(first, clean_url)
    company_url_in = Compose(first, clean_url)
    company_logo_urls_out = Compose(set, list)
    description_html_out = Compose(join)
    employment_types_out = Identity()
    locations_raw_out = Compose(set, list)
    source_urls_out = Identity()
