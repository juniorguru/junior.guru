import asyncio

import click
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


def parse_country_codes(
    context: click.Context, param: click.Parameter, value: str
) -> set[str]:
    country_codes = {code.strip().upper() for code in value.split(",")}
    country_codes.discard("")
    if not country_codes:
        raise click.BadParameter("Provide at least one country code")
    return country_codes


@cli.sync_command(dependencies=["jobs-listing"])
@async_command
@click.option(
    "--country-codes",
    default="CZ,SK",
    callback=parse_country_codes,
    show_default=True,
)
async def main(country_codes: set[str]):
    with db.connection_context():
        jobs = list(ListedJob.listing())

    values = await asyncio.gather(
        *[asyncio.create_task(locate_list(job.locations_raw)) for job in jobs]
    )

    with db.connection_context():
        for job, value in zip(jobs, values):
            logger.info(f"Processing {job.url}")
            logger.info(
                f"Locations normalized: {job.locations_raw} → {value.locations} (universal: {value.is_universal})"
            )
            if is_relevant_country(value, country_codes):
                job.locations = [location.model_dump() for location in value.locations]
                job.remote = job.remote or value.is_universal
                job.save()
            else:
                logger.warning("Deleting the job as not relevant!")
                job.delete_instance()


async def locate_list(locations_raw: list[str]) -> LocationsList:
    if locations_raw:
        to_locate = [loc for loc in locations_raw if not is_universal_location(loc)]
        is_universal = len(to_locate) < len(locations_raw)
        locations = await asyncio.gather(
            *[asyncio.create_task(locate(location)) for location in to_locate]
        )
        return LocationsList(locations=locations, is_universal=is_universal)
    return LocationsList()


def is_relevant_country(locations_list: LocationsList, country_codes: set[str]) -> bool:
    if locations_list.is_universal:
        return True
    return any(
        location.country_code in country_codes for location in locations_list.locations
    )
