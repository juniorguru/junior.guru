from urllib.parse import urlencode

from scrapy import Request
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst

from juniorguru.scrapers.items import Job, first, parse_relative_time, split
from juniorguru.lib.url_params import increment_param, strip_params, get_param


class Spider(BaseSpider):
    name = 'linkedin'
    custom_settings = {
        'USER_AGENT': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) '
                       'Gecko/20100101 Firefox/75.0'),
        'ROBOTSTXT_OBEY': False,
    }
    search_params = {
        'keywords': 'Software Engineer',
        'location': 'Czech Republic',
        'f_E': '1,2',  # entry level, internship
        'f_TP': '1,2,3,4',  # past month
        'redirect': 'false',  # ?
        'position': '1',  # the job ad position to display as open
        'pageNum': '0',  # pagination - page number
        'start': '0',  # pagination - offset
    }
    start_urls = [
        ('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/'
         f'search?{urlencode(search_params)}')
    ]
    results_per_request = 25

    def parse(self, response):
        links = response.css('a[href*="linkedin.com/jobs/view/"]::attr(href)').getall()
        links = [strip_params(link, ['position', 'pageNum']) for link in links]
        yield from response.follow_all(links, callback=self.parse_job)

        if len(links) >= self.results_per_request:
            url = increment_param(response.url, 'start', self.results_per_request)
            yield Request(url, callback=self.parse)

    def parse_job(self, response):
        loader = Loader(item=Job(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_css('link', '.apply-button::attr(href)')
        loader.add_value('link', response.url)
        loader.add_css('company_name', 'h1 ~ h3 a::text')
        loader.add_css('company_name', 'h1 ~ h3 span::text')
        loader.add_css('company_link', 'h1 ~ h3 a::attr(href)')
        loader.add_css('location', 'h1 ~ h3 > span:nth-of-type(2)::text')
        loader.add_xpath('employment_types', "//h3[contains(., 'Employment type')]/following-sibling::span/text()")
        loader.add_xpath('experience_levels', "//h3[contains(., 'Seniority level')]/following-sibling::span/text()")
        loader.add_css('posted_at', 'h1 ~ h3:nth-of-type(2) span::text')
        loader.add_css('description_html', '.description__text')
        loader.add_css('company_logo_urls', 'img.company-logo::attr(src)')
        loader.add_css('company_logo_urls', 'img.company-logo::attr(data-delayed-url)')
        yield loader.load_item()


def parse_proxied_url(url):
    proxied_url = get_param(url, 'url')
    if proxied_url:
        param_names = ['utm_source', 'utm_medium', 'utm_campaign']
        return strip_params(proxied_url, param_names)
    return url


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    link_in = Compose(first, parse_proxied_url)
    employment_types_in = MapCompose(str.lower, split)
    employment_types_out = Identity()
    posted_at_in = Compose(first, parse_relative_time)
    experience_levels_in = MapCompose(str.lower, split)
    experience_levels_out = Identity()
    company_logo_urls_out = Identity()
