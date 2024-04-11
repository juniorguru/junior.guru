from jg.core.sync.jobs_scraped import DropItem


async def process(item: dict) -> dict:
    if llm_opinion := item.get("llm_opinion"):
        if is_entry_level := llm_opinion.get("is_entry_level"):
            return item

        text = "Not for juniors: "
        if is_entry_level is None:
            text += "missing opinion"
        elif is_entry_level is False:
            if reason := llm_opinion.get("reason"):
                text += reason
            else:
                text += "missing reason"
        raise DropItem(text)
    raise DropItem("Missing LLM opinion")
