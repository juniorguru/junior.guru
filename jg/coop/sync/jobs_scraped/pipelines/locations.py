import asyncio

from jg.coop.lib import loggers
from jg.coop.lib.async_utils import call_async
from jg.coop.lib.locations import fetch_locations


logger = loggers.from_path(__file__)


limit = asyncio.Semaphore(3)


async def process(item: dict) -> dict:
    if locations_raw := item.get("locations_raw"):
        logger.debug(f"Normalizing locations: {locations_raw!r}")
        debug_info = {
            "title": item.get("title"),
            "company_name": item.get("company_name"),
        }
        async with limit:
            locations = await call_async(
                fetch_locations,
                locations_raw,
                debug_info=debug_info,
            )
        logger.debug(f"Locations normalized: {locations_raw} → {locations}")
        item["locations"] = locations
    return item
