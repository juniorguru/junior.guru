from pprint import pformat

from juniorguru.lib import loggers
from juniorguru.lib.text import extract_text


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    try:
        item["description_text"] = extract_text(item["description_html"])
    except Exception:
        logger.error(f"Unable to extract text from item:\n{pformat(item)}")
        raise
    return item
