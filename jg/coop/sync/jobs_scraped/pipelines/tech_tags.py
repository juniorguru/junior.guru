from jg.beak.core import beak

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    item["tech_tags"] = beak(item["description_text"])
    return item
