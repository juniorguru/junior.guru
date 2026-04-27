import asyncio

from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.location import Location, is_universal_location, locate
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob


logger = loggers.from_path(__file__)


class LocationsList(BaseModel):
    locations: list[Location] = []
    is_universal: bool = False


@cli.sync_command(dependencies=["jobs-listing"])
@async_command
async def main():
    with db.connection_context():
        jobs = list(ListedJob.listing())

    values = await asyncio.gather(
        *[asyncio.create_task(locate_list(job.locations_raw)) for job in jobs]
    )

    with db.connection_context():
        for job, value in zip(jobs, values):
            logger.info(
                f"Locations normalized: {job.locations_raw} → {value.locations} (universal: {value.is_universal})"
            )
            job.locations = [location.model_dump() for location in value.locations]
            job.remote = job.remote or value.is_universal
            job.save()


async def locate_list(locations_raw: list[str]) -> LocationsList:
    if locations_raw:
        to_locate = [loc for loc in locations_raw if not is_universal_location(loc)]
        is_universal = len(to_locate) < len(locations_raw)
        locations = await asyncio.gather(
            *[asyncio.create_task(locate(location)) for location in to_locate]
        )
        return LocationsList(locations=locations, is_universal=is_universal)
    return LocationsList()
