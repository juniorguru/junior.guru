import emoji


def remove_emoji(text: str):
    return strip_whitespace(emoji.replace_emoji(strip_whitespace(text), replace=""))


def strip_whitespace(text: str):
    previous = text
    while True:
        stripped = previous
        stripped = stripped.strip()
        stripped = stripped.strip("\u200d")

        if stripped == previous:
            return stripped
        previous = stripped
