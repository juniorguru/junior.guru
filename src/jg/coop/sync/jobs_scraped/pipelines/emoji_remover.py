from jg.coop.lib.text import remove_emoji


async def process(item: dict) -> dict:
    title = item["title"]
    try:
        item["title"] = remove_emoji(title)
        return item
    except Exception as e:
        raise ValueError(f"Failed to remove emojis in {item['title']!r}") from e
