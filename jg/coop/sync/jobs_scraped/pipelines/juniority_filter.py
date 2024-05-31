from jg.coop.sync.jobs_scraped import DropItem


async def process(item: dict) -> dict:
    if llm_opinion := item.get("llm_opinion"):
        if llm_opinion["is_entry_level"]:
            return item
        raise DropItem(f"Not for juniors: {llm_opinion['reason_cs']!r}")
    raise DropItem("Missing LLM opinion")
