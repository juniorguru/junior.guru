import langdetect
from juniorguru.lib import loggers
from w3lib.html import remove_tags


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    item["lang"] = parse_language(item["description_html"])
    return item


def parse_language(description_html: str) -> str:
    return langdetect.detect(remove_tags(description_html))
