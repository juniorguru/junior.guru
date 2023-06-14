import emoji


def process(item):
    title = item['title']
    try:
        item['title'] = strip(emoji.replace_emoji(strip(title), replace=''))
        return item
    except Exception as e:
        raise ValueError(f"Failed to clean emojis in {item['title']!r}") from e


def strip(original):
    previous = original
    while True:
        stripped = previous
        stripped = stripped.strip()
        stripped = stripped.strip('\u200d')

        if stripped == previous:
            return stripped
        previous = stripped
