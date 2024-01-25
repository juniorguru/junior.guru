from diskcache import Cache

from juniorguru.lib.remove_emoji import remove_emoji


async def process(item: dict, cache: Cache | None = None) -> dict:
    title = item["title"]
    try:
        item["title"] = remove_emoji(title)
        return item
    except Exception as e:
        raise ValueError(f"Failed to remove emojis in {item['title']!r}") from e
