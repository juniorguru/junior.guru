import re
from datetime import datetime, timedelta

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity

from ..items import Job
from ..processors import absolute_url


class Spider(scrapy.Spider):
    name = 'stackoverflow'
    start_urls = [
        'https://stackoverflow.com/jobs?mxs=Junior&sort=p&l=Seč%2C+Czechia&d=350&u=Km'
    ]

    def parse(self, response):
        links = response.css('.-job h2 a')
        yield from response.follow_all(links, callback=self.parse_job)

        links = response.xpath("//a[contains(@class, 's-pagination--item')]")
        yield from response.follow_all(links, callback=self.parse)

    def parse_job(self, response):
        loader = Loader(item=Job(), response=response)
        loader.add_css('title', 'h1 a::text')
        loader.add_value('link', response.url)
        loader.add_css('company_name', 'h1 ~ div a::text')
        loader.add_css('company_link', 'h1 ~ div a::attr(href)')
        loader.add_css('location_raw', 'h1 ~ div a ~ span::text')
        loader.add_xpath('employment_types', "//span[contains(., 'Job type:')]/following-sibling::span/text()")  # Full-time, Internship, Contract
        loader.add_xpath('timestamp', "//div[contains(./text(), 'Posted')]/text()")
        loader.add_xpath('description_raw', "//section[contains(.//h2/text(), 'Job description')]")
        yield loader.load_item()


def clean_location_raw(text):
    return re.sub(r'^–\s*', '', re.sub(r'[\n\r]+', ' ', text.strip()))


def parse_relative_time(text, now=None):
    now = now or datetime.utcnow()
    if 'hour' in text:
        return now
    if 'yesterday' in text:
        return now - timedelta(days=1)
    if 'day' in text:
        days_ago = int(re.search(r'\d+', text).group(0))
        return now - timedelta(days=days_ago)
    raise ValueError(text)


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    company_link_in = MapCompose(absolute_url)
    employment_types_out = Identity()
    location_raw_in = MapCompose(clean_location_raw)
    timestamp_in = MapCompose(parse_relative_time)
