from datetime import date, timedelta

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers
from jg.coop.lib.cache import cache
from jg.coop.lib.mutations import MutationsNotAllowedError
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob, ScrapedJob, SubmittedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-scraped", "jobs-submitted"])
@click.option("--actor", "actor_name", default="honzajavorek/job-checks")
@db.connection_context()
def main(actor_name: str):
    ListedJob.drop_table()
    ListedJob.create_table()

    listing_date = date.today()
    logger.info(f"Processing submitted jobs: {listing_date}")
    submitted_jobs = SubmittedJob.date_listing(listing_date)
    for submitted_job in submitted_jobs:
        logger.debug(f"Listing {submitted_job!r}")
        job = submitted_job.to_listed()
        job.save()
        logger.debug(f"Saved {submitted_job!r} as {job!r}")

    logger.info("Processing scraped jobs")
    scraped_jobs = list(ScrapedJob.listing())
    try:
        logger.info(f"Running checks for {len(scraped_jobs)} URLs")
        checks = logger.wait(check_jobs, actor_name, [job.url for job in scraped_jobs])
    except MutationsNotAllowedError:
        logger.warning("Not allowed to check for expired jobs, relying on stale data")
        checks = apify.fetch_data(actor_name)
    if len(checks) != len(scraped_jobs):
        logger.warning(
            f"Number of checks ({len(checks)}) does not match "
            f"the number of scraped jobs ({len(scraped_jobs)})!"
        )

    status_by_url = {check["url"]: check["ok"] for check in checks}
    for scraped_job in scraped_jobs:
        status = status_by_url.get(scraped_job.url, None)
        status_for_humans = {
            None: "N/A",
            True: "OK",
            False: "EXPIRED",
        }[status]
        logger.info(f"{status_for_humans} - {scraped_job.url}")
        if status is not False:
            logger.debug(f"Listing {scraped_job!r}")
            job = scraped_job.to_listed()
            job.save()
            logger.debug(f"Saved {scraped_job!r} as {job!r}")


@cache(expire=timedelta(hours=6), tag="job-checks")
def check_jobs(actor_name: str, urls: list[str]) -> list[dict]:
    return apify.run(actor_name, {"links": [{"url": url} for url in urls]})
