import re
from json import JSONDecodeError

from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, MapCompose, TakeFirst

from juniorguru.jobs.items import Job, absolute_url, parse_iso_date, parse_markdown


class Spider(BaseSpider):
    name = 'remoteok'
    custom_settings = {'DOWNLOAD_DELAY': 1}
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
            url = json_data['url'].replace(json_data['id'], json_data['slug'])
            yield response.follow(url,
                                  callback=self.parse_job,
                                  cb_kwargs=dict(json_data=json_data))

    def parse_job(self, response, json_data):
        loader = Loader(item=Job(), response=response)
        loader.add_value('source', self.name)
        loader.add_value('source_urls', response.url)
        loader.add_value('title', json_data['position'])
        loader.add_value('url', response.url)
        loader.add_value('company_name', json_data['company'])
        loader.add_css('company_url', '*[itemprop="hiringOrganization"]::attr(href)')
        loader.add_value('remote_region_raw', json_data['location'])
        loader.add_value('remote', True)
        loader.add_value('posted_at', json_data['date'])
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
    posted_at_in = MapCompose(parse_iso_date)
    description_html_in = MapCompose(fix_newlines, parse_markdown)
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
    source_urls_out = Identity()
