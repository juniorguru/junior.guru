from datetime import date

from project.cli.sync import main as cli
from project.lib import loggers
from project.models.base import db
from project.models.job import ListedJob, ScrapedJob, SubmittedJob


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

    listing_date = ScrapedJob.latest_posted_on()
    logger.info(f"Processing scraped jobs: {listing_date}")
    query = ScrapedJob.date_listing(listing_date)
    for scraped_job in query.iterator():
        logger.debug(f"Listing {scraped_job!r}")
        job = scraped_job.to_listed()
        job.save()
        logger.debug(f"Saved {scraped_job!r} as {job!r}")
