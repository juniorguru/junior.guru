import asyncio

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.location import Location, locate
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-listing"])
@async_command
async def main():
    with db.connection_context():
        jobs = list(ListedJob.listing())

    values = await asyncio.gather(
        *[asyncio.create_task(locate_list(job.locations_raw)) for job in jobs]
    )

    with db.connection_context():
        for job, locations in zip(jobs, values):
            logger.info(f"Locations normalized: {job.locations_raw} → {locations}")
            job.locations = [location.model_dump() for location in locations]
            job.save()


async def locate_list(locations_raw: list[str]) -> list[Location]:
    if locations_raw:
        return await asyncio.gather(
            *[asyncio.create_task(locate(location)) for location in locations_raw]
        )
    return []
