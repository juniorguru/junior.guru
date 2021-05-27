import re
from urllib.parse import urlencode, urlparse

from scrapy import Request
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst

from juniorguru.scrapers.items import Job, first, parse_relative_date, split
from juniorguru.lib.url_params import increment_param, strip_params, get_param, replace_in_params


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
        'https://www.jobs.cz/prace/?field%5B%5D=200900013&field%5B%5D=200900012&suitable-for=graduates',
    ]

    def parse(self, response):
        links = response.css('a[data-link="jd-detail"]::attr(href)').getall()
        yield from response.follow_all(links, callback=self.parse_job)

    def parse_job(self, response):
        if 'www.jobs.cz' not in response.url:  # TODO custom job portals
            return

        loader = Loader(item=Job(), response=response)
        loader.add_css('title', 'h1::text')  # TODO split by |
        # loader.add_css('remote', 'h2::text')
        loader.add_value('link', response.url)
        loader.add_css('company_name', '.topcard__org-name-link::text')
        loader.add_css('company_name', '.topcard__content-left > h3 > span:nth-of-type(1)::text')
        loader.add_css('company_link', '.topcard__org-name-link::attr(href)')
        loader.add_css('locations_raw', '.topcard__content-left > h3:nth-of-type(1) > span:nth-of-type(2)::text')
        loader.add_xpath('employment_types', "//h3[contains(., 'Employment type')]/following-sibling::span/text()")
        loader.add_xpath('experience_levels', "//h3[contains(., 'Seniority level')]/following-sibling::span/text()")
        loader.add_css('posted_at', '.topcard__content-left > h3:nth-of-type(2) span::text')
        loader.add_css('description_html', '.description__text')
        loader.add_css('company_logo_urls', 'img.company-logo::attr(src)')
        loader.add_css('company_logo_urls', 'img.company-logo::attr(data-delayed-url)')
        item = loader.load_item()

        if not item.get('link') or 'linkedin.com' in item['link']:
            yield item
        else:
            yield response.follow(item['link'],
                                  callback=self.verify_job,
                                  cb_kwargs=dict(item=item))

    def verify_job(self, response, item):
        """Filters out links to broken external links"""
        yield item


def get_job_id(url):
    return re.search(r'-(\d+)$', urlparse(url).path).group(1)


def clean_proxied_url(url):
    proxied_url = get_param(url, 'url')
    if proxied_url:
        param_names = ['utm_source', 'utm_medium', 'utm_campaign']
        proxied_url = strip_params(proxied_url, param_names)
        return replace_in_params(proxied_url, 'linkedin', 'juniorguru',
                                 case_insensitive=True)
    return url


def clean_url(url):
    if url and 'linkedin.com' in url:
        return strip_params(url, ['refId', 'trk'])
    if url and 'talentify.io' in url:
        return strip_params(url, ['tdd'])
    if url and 'neuvoo.cz' in url:
        return strip_params(url, ['puid'])
    if url and 'lever.co' in url:
        return re.sub(r'/apply$', '/', url)
    return url


def parse_remote(text):
    return bool(re.search(r'\bremote\b', text, re.IGNORECASE))


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    link_in = Compose(first, clean_proxied_url, clean_url)
    company_link_in = Compose(first, clean_url)
    employment_types_in = MapCompose(str.lower, split)
    employment_types_out = Identity()
    posted_at_in = Compose(first, parse_relative_date)
    experience_levels_in = MapCompose(str.lower, split)
    experience_levels_out = Identity()
    company_logo_urls_out = Identity()
    remote_in = MapCompose(parse_remote)
    locations_raw_out = Identity()
