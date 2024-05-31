from jg.coop.sync.jobs_scraped import DropItem
from jg.coop.sync.jobs_scraped.pipelines.llm_opinion import LLMOpinion


async def process(item: dict) -> dict:
    llm_opinion: LLMOpinion = item.get("llm_opinion")
    if llm_opinion:
        if llm_opinion.is_entry_level:
            return item
        raise DropItem(f"Not for juniors: {llm_opinion.reason_cs!r}")
    raise DropItem("Missing LLM opinion")
