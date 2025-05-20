import re
from datetime import timedelta
from typing import Annotated

from openai import BaseModel
from pydantic import HttpUrl, PlainSerializer
from yt_dlp import YoutubeDL

from jg.coop.lib.cache import cache


YOUTUBE_URL_RE = re.compile(
    r"(youtube\.com.+watch\?.*v=|youtube\.com/live/|youtu\.be/)([\w\-\_]+)"
)


class YouTubeInfo(BaseModel):
    id: str
    url: Annotated[HttpUrl, PlainSerializer(str)]
    title: str
    title_full: str
    thumbnail_url: Annotated[HttpUrl, PlainSerializer(str)]
    description: str
    duration_s: int
    view_count: int
    comment_count: int
    like_count: int
    chapters: list[str]


def parse_youtube_id(url) -> str:
    match = YOUTUBE_URL_RE.search(url)
    try:
        return match.group(2)
    except AttributeError:
        raise ValueError(f"URL {url} doesn't contain YouTube ID")


def get_youtube_url(youtube_id: str) -> str:
    return f"https://www.youtube.com/watch?v={youtube_id}"


def parse_youtube_info(info: dict) -> YouTubeInfo:
    return YouTubeInfo(
        id=info["id"],
        url=info["webpage_url"],
        title=info["title"],
        title_full=info["fulltitle"],
        thumbnail_url=info["thumbnail"],
        description=info["description"],
        duration_s=info["duration"],
        view_count=info["view_count"],
        comment_count=info["comment_count"] or 0,
        like_count=info["like_count"] or 0,
        chapters=[chapter["title"] for chapter in info["chapters"] or []],
    )


@cache(expire=timedelta(hours=12), tag="youtube-info")
def fetch_youtube_info(youtube_url: str) -> YouTubeInfo:
    with YoutubeDL({"quiet": True, "no_warnings": True}) as yt:
        return yt.extract_info(youtube_url, download=False)
