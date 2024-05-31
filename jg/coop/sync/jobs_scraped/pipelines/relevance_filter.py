from jg.coop.sync.jobs_scraped import DropItem


async def process(item: dict) -> dict:
    if llm_opinion := item.get("llm_opinion"):
        if llm_opinion["fields"]:
            return item
        raise DropItem("Not relevant")
    raise DropItem("Missing LLM opinion")
