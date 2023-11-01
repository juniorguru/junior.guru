from juniorguru.lib.remove_emoji import remove_emoji


def process(item):
    title = item["title"]
    try:
        item["title"] = remove_emoji(title)
        return item
    except Exception as e:
        raise ValueError(f"Failed to remove emojis in {item['title']!r}") from e
