from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    return item
