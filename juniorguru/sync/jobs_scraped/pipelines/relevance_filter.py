from juniorguru.sync.jobs_scraped import DropItem


async def process(item: dict) -> dict:
    if llm_opinion := item.get("llm_opinion"):
        is_sw_engineering = llm_opinion.get("is_sw_engineering")
        is_sw_testing = llm_opinion.get("is_sw_testing")

        if is_sw_engineering or is_sw_testing:
            return item

        text = "Not relevant: "
        if is_sw_engineering is None:
            text += "missing opinion on SW engineering"
        elif is_sw_engineering is False:
            text += "not SW engineering"
        text += ", "
        if is_sw_testing is None:
            text += "missing opinion on SW testing"
        elif is_sw_testing is False:
            text += "not SW testing"
        raise DropItem(text)
    raise DropItem("Missing LLM opinion")
