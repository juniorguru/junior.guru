import langdetect
from juniorguru.lib import loggers
from w3lib.html import remove_tags

from juniorguru.lib.async_utils import call_async


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    item["lang"] = await call_async(parse_language, item["description_html"])
    return item


def parse_language(description_html: str) -> str:
    return langdetect.detect(remove_tags(description_html))
