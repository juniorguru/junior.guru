from datetime import date

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob, ScrapedJob, SubmittedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-scraped", "jobs-submitted"])
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

    logger.info("Processing scraped jobs")
    query = ScrapedJob.listing()
    for scraped_job in query.iterator():
        logger.debug(f"Listing {scraped_job!r}")
        job = scraped_job.to_listed()
        job.save()
        logger.debug(f"Saved {scraped_job!r} as {job!r}")
