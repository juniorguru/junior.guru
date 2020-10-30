from urllib.parse import urlencode

from scrapy import Request
from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, Identity, MapCompose, TakeFirst

from juniorguru.scrapers.items import Job, first, parse_relative_date, split
from juniorguru.lib.url_params import increment_param, strip_params, get_param, replace_in_params


class Spider(BaseSpider):
    name = 'linkedin'
    proxy = True
    download_delay = 1
    download_timeout = 40
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'cs,en',
        },
        'USER_AGENT': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) '
                       'Gecko/20100101 Firefox/75.0'),
        'ROBOTSTXT_OBEY': False,
    }

    search_terms = [
        'Software Engineer',
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
        links = response.css('a[href*="linkedin.com/jobs/view/"]::attr(href)').getall()
        links = [strip_params(link, ['position', 'pageNum', 'trk', 'refId'])
                 for link in links]
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
        loader.add_css('location_raw', 'h1 ~ h3 > span:nth-of-type(2)::text')
        loader.add_value('remote', False)
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
        proxied_url = strip_params(proxied_url, param_names)
        return replace_in_params(proxied_url, 'linkedin', 'juniorguru',
                                 case_insensitive=True)
    return url


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    link_in = Compose(first, parse_proxied_url)
    employment_types_in = MapCompose(str.lower, split)
    employment_types_out = Identity()
    posted_at_in = Compose(first, parse_relative_date)
    experience_levels_in = MapCompose(str.lower, split)
    experience_levels_out = Identity()
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
