from juniorguru.lib import loggers
from juniorguru.sync.jobs_scraped import DropItem


logger = loggers.from_path(__file__)


RELEVANT_LANGS = ["cs", "en"]


async def process(item: dict) -> dict:
    if item["lang"] not in RELEVANT_LANGS:
        raise DropItem(
            f"Language detected as '{item['lang']}' (relevant: {', '.join(RELEVANT_LANGS)})"
        )
    return item
