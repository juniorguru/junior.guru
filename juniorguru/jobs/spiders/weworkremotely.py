import json
import html
import time
from datetime import datetime

import arrow
import extruct
import feedparser
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, MapCompose, TakeFirst

from juniorguru.jobs.items import Job, absolute_url


class Spider(BaseSpider):
    name = 'weworkremotely'
    start_urls = [
        'https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss',
        'https://weworkremotely.com/categories/remote-programming-jobs.rss',
    ]

    def parse(self, response):
        for entry in feedparser.parse(response.text).entries:
            feed_data = dict(title=entry.title,
                             posted_at=parse_struct_time(entry.published_parsed),
                             remote_region_raw=entry.region,
                             company_logo_urls=[c['url'] for c in getattr(entry, 'media_content', [])],
                             description_html=entry.summary,
                             remote=True,
                             source_urls=response.url)
            yield response.follow(entry.link,
                                  callback=self.parse_job,
                                  cb_kwargs=dict(feed_data=feed_data))

    def parse_job(self, response, feed_data):
        loader = Loader(item=Job(), response=response)
        loader.add_value('url', response.url)

        for key, value in feed_data.items():
            loader.add_value(key, value)

        try:
            data = extract_job_posting(response.text, response.url)
            loader.add_value('source', self.name)
            loader.add_value('source_urls', response.url)
            loader.add_value('title', data['title'])
            loader.add_value('posted_at', data['datePosted'])
            loader.add_value('description_html', html.unescape(data['description']))
            loader.add_value('company_logo_urls', data.get('image'))
            loader.add_value('employment_types', [data['employmentType']])
            loader.add_value('company_name', data['hiringOrganization']['name'])
            loader.add_value('company_url', data['hiringOrganization']['sameAs'])
            loader.add_value('locations_raw', data['hiringOrganization']['address'])
            yield loader.load_item()
        except json.JSONDecodeError:
            pass


def parse_struct_time(struct_time):
    if struct_time:
        return datetime.fromtimestamp(time.mktime(struct_time)).date()


def parse_date(value):
    try:
        return arrow.get(value).date()
    except ValueError:
        return arrow.get(value, 'YYYY-MM-DD HH:mm:ss ZZZ').date()


def extract_job_posting(html_string, base_url):
    data = extruct.extract(html_string, base_url, syntaxes=['json-ld'])
    return next(data_item for data_item in data['json-ld']
                if data_item['@type'] == 'JobPosting')


class Loader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    company_url_in = MapCompose(absolute_url)
    posted_at_in = MapCompose(parse_date)
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
    locations_raw_out = Identity()
    source_urls_out = Identity()
