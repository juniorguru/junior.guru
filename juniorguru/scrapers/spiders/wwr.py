from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, MapCompose, TakeFirst

from juniorguru.scrapers.items import Job, absolute_url, parse_iso_date


class Spider(BaseSpider):
    name = 'wwr'
    start_urls = [
        'https://weworkremotely.com/categories/remote-devops-sysadmin-jobs',
        'https://weworkremotely.com/categories/remote-programming-jobs',
    ]

    def parse(self, response):
        for link in response.css('.feature a[href*="/remote-jobs/"]'):
            yield response.follow(link, callback=self.parse_job)

    def parse_job(self, response):
        loader = Loader(item=Job(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('link', response.url)
        loader.add_css('company_name', '.company-card h2 a::text')
        loader.add_css('company_link', '.company-card a::attr(href)')
        loader.add_css('location_raw', '.company-card h2 ~ h3::text')
        loader.add_value('remote', True)
        loader.add_css('posted_at', '.content time::attr(datetime)')
        loader.add_css('description_html', '#job-listing-show-container')
        loader.add_css('company_logo_urls', '.company-card .listing-logo img::attr(src)')
        yield loader.load_item()


class Loader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    company_link_in = MapCompose(absolute_url)
    posted_at_in = MapCompose(parse_iso_date)
    company_logo_urls_out = Identity()
    remote_in = MapCompose(bool)
