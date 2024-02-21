from datetime import date, timedelta
from juniorguru.sync.jobs_scraped import DropItem


async def process(item: dict, today: date | None = None, days=90) -> dict:
    today = today or date.today()
    min_date = today - timedelta(days=days)
    if item["posted_on"] < min_date:
        raise DropItem(f"Older than {days} days: {item['posted_on']}")
    return item
