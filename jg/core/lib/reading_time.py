import math


def reading_time(content_size: int) -> int:
    if not content_size:
        return 1
    norm_pages = content_size / 1800  # see https://cs.wikipedia.org/wiki/Normostrana
    words_count = (
        norm_pages * 250
    )  # estimate, see https://cs.wikipedia.org/wiki/Normostrana
    return math.ceil(words_count / 200)  # 200 words per minute
