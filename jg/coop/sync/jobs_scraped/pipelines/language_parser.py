from jg.coop.lib import loggers
from jg.coop.lib.lang import async_parse_language


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    item["lang"] = await async_parse_language(item["description_text"])
    return item
