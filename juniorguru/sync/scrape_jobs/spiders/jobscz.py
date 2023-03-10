from datetime import date
from urllib.parse import urljoin

from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader

from juniorguru.lib import loggers
from juniorguru.lib.url_params import strip_params
from juniorguru.sync.scrape_jobs.items import Job, first, split


logger = loggers.from_path(__file__)


class Spider(BaseSpider):
    name = 'jobscz'
    proxy = True
    download_timeout = 15
    custom_settings = {'ROBOTSTXT_OBEY': False}
    start_urls = [
        'https://beta.www.jobs.cz/prace/programator/',
        'https://beta.www.jobs.cz/prace/tester/',
    ]

    employment_types_labels = [
        'Typ pracovního poměru',
        'Employment form',
    ]

    def parse(self, response):
        card_xpath = "//article[contains(@class, 'SearchResultCard')]"
        for n, card in enumerate(response.xpath(card_xpath), start=1):
            url = card.css('a[data-link="jd-detail"]::attr(href)').get()
            loader = Loader(item=Job(), response=response)
            card_loader = loader.nested_xpath(f'{card_xpath}[{n}]')
            card_loader.add_value('source', self.name)
            card_loader.add_value('first_seen_on', date.today())
            card_loader.add_css('title', 'h2 a::text')
            card_loader.add_css('company_name', '.SearchResultCard__footerItem:nth-child(1) span::text')
            card_loader.add_css('company_logo_urls', '.CompanyLogo img::attr(src)')
            card_loader.add_css('locations_raw', '.SearchResultCard__footerItem:nth-child(2)::text')
            card_loader.add_value('source_urls', response.url)
            card_loader.add_value('source_urls', url)
            item = loader.load_item()
            yield response.follow(url, callback=self.parse_job, cb_kwargs=dict(item=item))
        logger.warning('Not implemented yet: pagination')

    def parse_job(self, response, item):
        loader = Loader(item=item, response=response)
        loader.add_value('url', response.url)
        loader.add_value('source_urls', response.url)
        if 'www.jobs.cz' not in response.url:
            yield from self.parse_job_custom(response, loader)
        elif response.css('.LayoutGrid--cassiopeia').get():
            yield from self.parse_job_standard(response, loader)
        else:
            yield from self.parse_job_company(response, loader)

    def parse_job_standard(self, response, loader):
        for label in self.employment_types_labels:
            loader.add_xpath('employment_types', f"//span[contains(text(), {label!r})]/following-sibling::p/text()")
        loader.add_xpath('description_html', "//p[contains(@class, 'typography-body-medium-text-regular')][contains(text(), 'Úvodní představení')]/following-sibling::p")
        loader.add_xpath('description_html', "//p[contains(@class, 'typography-body-medium-text-regular')][contains(text(), 'Pracovní nabídka')]/following-sibling::*")
        yield loader.load_item()

    def parse_job_company(self, response, loader):
        for label in self.employment_types_labels:
            loader.add_xpath('employment_types', f"//span[contains(text(), {label!r})]/parent::dd/text()")
        loader.add_css('description_html', '.grid__item.e-16 .clearfix')
        loader.add_css('description_html', '.jobad__body')
        company_url_relative = response.css('.company-profile__navigation__link::attr(href)').get()
        loader.add_value('company_url', urljoin(response.url, company_url_relative))
        yield loader.load_item()

    def parse_job_custom(self, response, loader):
        logger.warning('Not implemented yet: custom job portals')
        if False:
            yield


def clean_url(url):
    return strip_params(url, ['positionOfAdInAgentEmail', 'searchId', 'rps'])


def join(values):
    return ''.join(values)


def remove_empty(values):
    return filter(None, values)


def remove_width_param(url):
    return strip_params(url, ['width'])


class Loader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    url_in = Compose(first, clean_url)
    company_url_in = Compose(first, clean_url)
    company_logo_urls_in = MapCompose(remove_width_param)
    company_logo_urls_out = Compose(set, list)
    description_html_out = Compose(join)
    employment_types_in = MapCompose(str.lower, split)
    employment_types_out = Identity()
    locations_raw_out = Compose(remove_empty, set, list)
    source_urls_out = Identity()
    first_seen_on_in = Identity()
