from datetime import date, timedelta

from jg.coop.sync.jobs_scraped import DropItem


async def process(item: dict, today: date | None = None, days=90) -> dict:
    posted_on = date.fromisoformat(item["posted_on"])
    threshold_on = (today or date.today()) - timedelta(days=days)
    if posted_on < threshold_on:
        raise DropItem(f"Older than {days} days: {posted_on}")
    return item
