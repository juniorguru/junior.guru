from datetime import date

import click

from juniorguru.lib import loggers
from juniorguru.cli.sync import ChainCommand
from juniorguru.models.base import db
from juniorguru.models.job import ListedJob, ScrapedJob, SubmittedJob


MIN_JUNIORITY_RE_SCORE = 1


logger = loggers.get(__name__)


@click.command(cls=ChainCommand, requires=['jobs-scraped',
                            'jobs-submitted'])
@db.connection_context()
def main():
    ListedJob.drop_table()
    ListedJob.create_table()

    listing_date = date.today()
    logger.info(f"Processing submitted jobs: {listing_date}")
    query = SubmittedJob.date_listing(listing_date)
    for submitted_job in query:
        logger.debug(f"Listing {submitted_job!r}")
        job = submitted_job.to_listed()
        job.save()
        logger.debug(f"Saved {submitted_job!r} as {job!r}")

    listing_date = ScrapedJob.latest_seen_on()
    logger.info(f"Processing scraped jobs: {listing_date}, juniority_re_score ≥ {MIN_JUNIORITY_RE_SCORE}")
    query = ScrapedJob.date_listing(listing_date,
                                    min_juniority_re_score=MIN_JUNIORITY_RE_SCORE)
    for scraped_job in query.iterator():
        logger.debug(f"Listing {scraped_job!r}")
        job = scraped_job.to_listed()
        job.save()
        logger.debug(f"Saved {scraped_job!r} as {job!r}")
