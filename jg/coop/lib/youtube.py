import re


YOUTUBE_URL_RE = re.compile(
    r"(youtube\.com.+watch\?.*v=|youtube\.com/live/|youtu\.be/)([\w\-\_]+)"
)


def parse_youtube_id(url) -> str:
    match = YOUTUBE_URL_RE.search(url)
    try:
        return match.group(2)
    except AttributeError:
        raise ValueError(f"URL {url} doesn't contain YouTube ID")
