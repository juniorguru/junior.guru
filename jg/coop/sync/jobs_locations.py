from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.locations import fetch_locations
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-listing"])
@db.connection_context()
def main():
    for job in ListedJob.listing():
        if locations_raw := job.locations_raw:
            logger.info(f"Normalizing locations: {locations_raw!r}")
            debug_info = {"title": job.title, "company_name": job.company_name}
            locations = fetch_locations(
                locations_raw,
                debug_info=debug_info,
            )
            logger.debug(f"Locations normalized: {locations_raw} → {locations}")
            job.locations = locations
            job.save()
