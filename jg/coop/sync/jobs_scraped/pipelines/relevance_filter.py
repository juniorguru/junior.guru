from jg.coop.sync.jobs_scraped import DropItem


async def process(item: dict) -> dict:
    if llm_opinion := item.get("llm_opinion"):
        if not llm_opinion["is_relevant"]:
            raise DropItem(f"Not relevant: {llm_opinion['reason']}")
        return item
    raise DropItem("Missing LLM opinion")
