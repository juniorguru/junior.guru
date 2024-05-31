from jg.coop.sync.jobs_scraped import DropItem
from jg.coop.sync.jobs_scraped.pipelines.llm_opinion import LLMOpinion


async def process(item: dict) -> dict:
    llm_opinion: LLMOpinion = item.get("llm_opinion")
    if llm_opinion:
        if llm_opinion.fields:
            return item
        raise DropItem("Not relevant")
    raise DropItem("Missing LLM opinion")
