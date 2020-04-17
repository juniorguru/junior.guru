import re
from datetime import datetime, timedelta

import scrapy


class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    start_urls = [
        'https://stackoverflow.com/jobs'
        '?mxs=Junior&sort=p&l=Seč%2C+Czechia&d=350&u=Km'
    ]

    def parse(self, response):
        links = response.css('.-job h2 a')
        yield from response.follow_all(links, callback=self.parse_job)

        links = response.xpath("//a[contains(@class, 's-pagination--item')]")
        yield from response.follow_all(links, callback=self.parse)

    def parse_job(self, response):
        yield {
            'title': response.css('h1 a::text').get(),
            'link': response.url,
            'company_name': response.css('h1 ~ div a::text').get(),
            'company_link': response.urljoin(response.css('h1 ~ div a::attr(href)').get()),
            'location_raw': parse_location_raw(response.css('h1 ~ div a ~ span::text').get()),
            'employment_types': [response.xpath("//span[contains(., 'Job type:')]/following-sibling::span/text()").get()],  # Full-time, Internship, Contract
            'timestamp': parse_timestamp(response.xpath("//div[contains(./text(), 'Posted')]/text()").get()),
            'description_raw': response.xpath("//section[contains(.//h2/text(), 'Job description')]").get(),
        }


def parse_location_raw(text):
    return re.sub(r'^–\s*', '', re.sub(r'[\n\r]+', ' ', text.strip()))


def parse_timestamp(text):
    if 'hour' in text:
        return datetime.utcnow()
    if 'yesterday' in text:
        return datetime.utcnow() - timedelta(days=1)
    if 'day' in text:
        days_ago = int(re.search(r'\d+', text).group(0))
        return datetime.utcnow() - timedelta(days=days_ago)
    raise ValueError(text)
