from scrapy import Spider as BaseSpider

from juniorguru.models import db, ScrapedJob, SubmittedJob, Company


# musi existovat nejaka tabulka JobPosting nebo JobListing nebo tak neco,
# podle ktery poznam ktery jobs (submitted/scraped) jsou vlastne potreba vyresit,
# ktery jsou vlastne aktualne na webu
#
# pak si vytahne z DB tyhlety jobs a companies a zkousi sparovat, jestli nahodou
# tahle firma nesponzoruje - v tom pripade propoji informaci a ulozi cestu k obrazku.
# jestli je nabidka highlighted se pocita podle toho, jestli sponzoruje klub nebo
# jestli je submitted.
#
# pro zbyle jobs chceme stahnout nejaky obrazek a to muzeme bud z urls ktery sou ulozeny
# v db ke kazdymu jobu, nebo se snazime najit nakej favicon?
#
# asi blbost, proste by se mely vzit firmy ze vsech jobs podle nazvu a urls k nim
# a nejak by se to melo resit pospolu


class Spider(BaseSpider):
    name = 'db'

    # tady bude file:// ... primo k tomuto souboru, proste takovej hack
    start_urls = [
        'https://remoteok.io/remote-dev-jobs.json?api=1',
    ]

    def start_requests(self):
        # https://stackoverflow.com/a/46339560/325365
        # https://docs.scrapy.org/en/latest/topics/spiders.html?highlight=start_requests#scrapy.spiders.Spider.start_requests
        pass

    def parse(self, response):
        pass
