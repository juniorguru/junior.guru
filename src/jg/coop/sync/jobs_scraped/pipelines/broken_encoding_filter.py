from jg.coop.lib import loggers
from jg.coop.sync.jobs_scraped import DropItem


logger = loggers.from_path(__file__)


async def process(item: dict, max_qm_count: int = 20) -> dict:
    qm_count = item["description_html"].count("?")
    if qm_count <= max_qm_count:
        return item
    raise DropItem(f"Found {qm_count} question marks (limit: {max_qm_count})")
