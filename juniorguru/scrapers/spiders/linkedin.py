import re
from urllib.parse import urlencode, urlparse

from scrapy import Request
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst

from juniorguru.scrapers.items import Job, first, parse_relative_date, split
from juniorguru.lib.url_params import increment_param, strip_params, get_param, replace_in_params


class Spider(BaseSpider):
    name = 'linkedin'
    proxy = True
    download_timeout = 59
    download_delay = 1.25
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
    }

    search_terms = [
        'Junior Software Engineer',
        'Junior Developer',
    ]
    results_per_request = 25

    def start_requests(self):
        base_url = 'https://cz.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'
        search_params = {
            'location': 'Czechia',
            'f_E': '1,2',  # entry level, internship
            'f_TP': '1,2,3,4',  # past month
            'redirect': 'false',  # ?
            'position': '1',  # the job ad position to display as open
            'pageNum': '0',  # pagination - page number
            'start': '0',  # pagination - offset
        }
        return (Request(f"{base_url}{urlencode({'keywords': term, **search_params})}",
                        dont_filter=True,
                        headers={'Accept-Language': 'cs;q=0.8,en;q=0.6'})
                for term in self.search_terms)

    def parse(self, response):
        links = [f'https://cz.linkedin.com/jobs-guest/jobs/api/jobPosting/{get_job_id(link)}' for link in
                 response.css('a[href*="linkedin.com/jobs/view/"]::attr(href)').getall()]
        yield from response.follow_all(links, callback=self.parse_job)

        if len(links) >= self.results_per_request:
            url = increment_param(response.url, 'start', self.results_per_request)
            yield Request(url, callback=self.parse)

    def parse_job(self, response):
        loader = Loader(item=Job(), response=response)
        loader.add_css('title', 'h2::text')
        loader.add_css('remote', 'h2::text')
        loader.add_css('link', '.apply-button::attr(href)')
        loader.add_css('link', '.topcard__content-left > a::attr(href)')
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
