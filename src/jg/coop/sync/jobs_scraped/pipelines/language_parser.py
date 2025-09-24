from jg.coop.lib import loggers
from jg.coop.lib.async_utils import call_async
from jg.coop.lib.lang import parse_language


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    item["lang"] = await call_async(parse_language, item["description_text"])
    return item
