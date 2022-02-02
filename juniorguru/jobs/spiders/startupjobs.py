import html

from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst

from juniorguru.jobs.items import Job, parse_iso_date
from juniorguru.lib.url_params import strip_utm_params


class Spider(BaseSpider):
    name = 'startupjobs'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # requesting API, so irrelevant, saving a few requests
    }
    start_urls = [
        'https://feedback.startupjobs.cz/feed/juniorguru.php'
    ]

    def parse(self, response):
        for n, offer in enumerate(response.xpath('//offer'), start=1):
            loader = Loader(item=Job(), response=response)
            offer_loader = loader.nested_xpath(f'//offer[{n}]')
            offer_loader.add_value('source', self.name)
            offer_loader.add_value('source_urls', response.url)
            offer_loader.add_xpath('title', './/position/text()')
            offer_loader.add_xpath('url', './/url/text()')
            offer_loader.add_xpath('apply_url', './/url/text()')
            offer_loader.add_xpath('company_name', './/startup/text()')
            offer_loader.add_xpath('company_url', './/startupURL/text()')
            offer_loader.add_xpath('locations_raw', './/city/text()')
            offer_loader.add_xpath('remote', ".//jobtype[contains(., 'Remote')]/text()")
            offer_loader.add_value('remote', False)
            offer_loader.add_xpath('employment_types', './/jobtype/text()')
            offer_loader.add_xpath('posted_at', './/lastUpdate//text()')
            offer_loader.add_xpath('description_html', './/description/text()')
            offer_loader.add_xpath('company_logo_urls', './/startupLogo/text()')
            yield loader.load_item()


def drop_remote(types):
    return [type_ for type_ in types if type_.lower() != 'remote']


class Loader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    title_in = MapCompose(html.unescape)
    url_in = MapCompose(str.strip, strip_utm_params)
    company_name_in = MapCompose(html.unescape)
    employment_types_in = Compose(MapCompose(str.strip), drop_remote)
    employment_types_out = Identity()
    posted_at_in = MapCompose(parse_iso_date)
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
    locations_raw_out = Identity()
    source_urls_out = Identity()
