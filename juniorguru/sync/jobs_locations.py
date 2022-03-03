from juniorguru.lib.tasks import sync_task
from juniorguru.models import db, ListedJob
from juniorguru.lib import loggers
from juniorguru.lib.locations import fetch_locations


MIN_JUNIORITY_RE_SCORE = 1


logger = loggers.get(__name__)


@sync_task()
@db.connection_context()
def main():
    for job in ListedJob.listing():
        logger.debug(f'Normalizing locations for {job!r}: {job.locations_raw!r}')
        job.locations = fetch_locations(job.locations_raw,
                                        debug_info=dict(title=job.title, company_name=job.company_name))
        logger.info(f'Locations for {job!r} normalized: {job.locations_raw} → {job.locations}')
        job.save()
