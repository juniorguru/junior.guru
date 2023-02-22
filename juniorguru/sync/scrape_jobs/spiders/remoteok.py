import re
from json import JSONDecodeError

from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader

from juniorguru.sync.scrape_jobs.items import (Job, absolute_url, parse_iso_date,
                                               parse_markdown)


class Spider(BaseSpider):
    name = 'remoteok'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # requesting API, so irrelevant, saving a few requests
        'DOWNLOAD_DELAY': 1,
    }
    start_urls = [
        'https://remoteok.io/remote-dev-jobs.json?api=1',
    ]

    def parse(self, response):
        try:
            json_data_list = response.json()
        except JSONDecodeError:
            if re.search(r'\bxdebug-error\b', response.text):
                return
            raise

        for json_data in json_data_list[1:]:  # skip legal notice
            yield response.follow(json_data['url'],
                                  callback=self.parse_job,
                                  cb_kwargs=dict(json_data=json_data))

    def parse_job(self, response, json_data):
        loader = Loader(item=Job(), response=response)
        loader.add_value('source', self.name)
        loader.add_value('source_urls', response.url)
        loader.add_value('title', json_data['position'])
        loader.add_value('url', response.url)
        loader.add_value('company_name', json_data['company'])
        loader.add_value('remote_region_raw', json_data['location'])
        loader.add_value('remote', True)
        loader.add_value('first_seen_on', json_data['date'])
        loader.add_css('description_html', '*[itemprop="description"] .markdown::text')
        loader.add_value('company_logo_urls', json_data['company_logo'] or None)
        yield loader.load_item()


def fix_newlines(value):
    if value:
        return re.sub(r'\\n', r'\n', value)


class Loader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    company_url_in = MapCompose(absolute_url)
    first_seen_on_in = MapCompose(parse_iso_date)
    description_html_in = MapCompose(fix_newlines, parse_markdown)
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
    source_urls_out = Identity()
