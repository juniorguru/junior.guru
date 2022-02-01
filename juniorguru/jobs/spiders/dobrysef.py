import os

from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, MapCompose, TakeFirst

from juniorguru.jobs.items import Job, absolute_url, parse_iso_date
from juniorguru.jobs.settings import DEFAULT_REQUEST_HEADERS


class Spider(BaseSpider):
    name = 'dobrysef'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Authorization': f"Bearer {os.environ.get('DOBRYSEF_API_KEY', '')}",
            **DEFAULT_REQUEST_HEADERS,
        }
    }
    start_urls = [
        'https://dobrysef.cz/api/v0/juniorguru/jobposts/',
    ]

    def parse(self, response):
        for json_data in response.json():
            yield self.parse_job(response, json_data)

    def parse_job(self, response, json_data):
        description_html = json_data['description_html']
        if json_data.get('is_junior_friendly'):  # hack to boost the description analysis
            description_html = 'junior\n\n' + description_html

        employment_types = []
        if json_data.get('is_full_time'):
            employment_types.append('full time')
        if json_data.get('is_part_time'):
            employment_types.append('part time')
        if json_data.get('is_contract_freelance'):
            employment_types.append('contract')

        loader = Loader(item=Job(), response=response)
        loader.add_value('title', json_data['title'])
        loader.add_value('link', json_data['url'])
        loader.add_value('company_name', json_data['org_name'])
        loader.add_value('company_link', json_data['org_url'])
        loader.add_value('remote', json_data['is_remote'])
        loader.add_value('posted_at', json_data['date_start']) # TODO
        loader.add_value('description_html', description_html)
        loader.add_value('company_logo_urls', json_data.get('org_logo_url') or None)
        loader.add_value('employment_types', employment_types)
        loader.add_value('locations_raw', json_data['cities'])
        return loader.load_item()


class Loader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    company_link_in = MapCompose(absolute_url)
    posted_at_in = MapCompose(parse_iso_date)
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
    employment_types_out = Identity()
    locations_raw_out = Identity()
