import re
from datetime import datetime
from typing import Annotated

from openai import BaseModel
from pydantic import HttpUrl, PlainSerializer
from yt_dlp import YoutubeDL


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
    duration: str
    duration_s: int
    view_count: int
    comment_count: int
    like_count: int
    tags: list[str]
    released_at: datetime
    uploaded_at: datetime
    chapters: list[str]


def parse_youtube_id(url) -> str:
    match = YOUTUBE_URL_RE.search(url)
    try:
        return match.group(2)
    except AttributeError:
        raise ValueError(f"URL {url} doesn't contain YouTube ID")


def parse_youtube_info(info: dict) -> YouTubeInfo:
    return YouTubeInfo(
        id=info["id"],
        url=info["webpage_url"],
        title=info["title"],
        title_full=info["fulltitle"],
        thumbnail_url=info["thumbnail"],
        description=info["description"],
        duration=info["duration_string"],
        duration_s=info["duration"],
        view_count=info["view_count"],
        comment_count=info.get("comment_count", 0),
        like_count=info.get("like_count", 0),
        tags=info.get("tags", []),
        released_at=datetime.fromtimestamp(info["release_timestamp"]),
        uploaded_at=datetime.fromtimestamp(info["timestamp"]),
        chapters=[chapter["title"] for chapter in info.get("chapters", [])],
    )


def fetch_youtube_info(url: str) -> YouTubeInfo:
    with YoutubeDL({"quiet": True, "no_warnings": True}) as yt:
        return yt.extract_info(url, download=False)
