from juniorguru.lib import loggers
from juniorguru.lib import timer
from juniorguru.jobs.employments import main as scrape_employments
from juniorguru.jobs.legacy_jobs import main as scrape_jobs
from juniorguru.jobs.proxies import main as scrape_proxies


logger = loggers.get('jobs')


@timer.notify
@timer.measure('jobs')
def main():
    scrape_employments()
    scrape_proxies()
    scrape_jobs()


main()
logger.info('Scraping done!')
