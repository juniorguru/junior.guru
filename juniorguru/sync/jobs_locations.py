from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.job import ListedJob
from juniorguru.lib import loggers
from juniorguru.lib.locations import fetch_locations
from juniorguru.sync.jobs_listing import main as jobs_listing_task


MIN_JUNIORITY_RE_SCORE = 1


logger = loggers.get(__name__)


@sync_task(jobs_listing_task)
@db.connection_context()
def main():
    for job in ListedJob.listing():
        if job.locations_raw:
            logger.debug(f'Normalizing locations for {job!r}: {job.locations_raw!r}')
            job.locations = fetch_locations(job.locations_raw,
                                            debug_info=dict(title=job.title, company_name=job.company_name))
            logger.info(f'Locations for {job!r} normalized: {job.locations_raw} → {job.locations}')
            job.save()
        else:
            logger.debug(f'Job {job!r} has no locations set')
