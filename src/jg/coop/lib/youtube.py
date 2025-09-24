import re
from datetime import timedelta
from typing import Annotated

from openai import BaseModel
from pydantic import HttpUrl, PlainSerializer

from jg.coop.lib import google_api
from jg.coop.lib.cache import cache


YOUTUBE_URL_RE = re.compile(
    r"(youtube\.com.+watch\?.*v=|youtube\.com/live/|youtu\.be/)([\w\-\_]+)"
)


class YouTubeInfo(BaseModel):
    id: str
    url: Annotated[HttpUrl, PlainSerializer(str)]
    title: str
    thumbnail_url: Annotated[HttpUrl, PlainSerializer(str)]
    description: str
    duration_s: int
    view_count: int
    comment_count: int
    like_count: int


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
        url=get_youtube_url(info["id"]),
        title=info["snippet"]["title"],
        thumbnail_url=info["snippet"]["thumbnails"]["maxres"]["url"],
        description=info["snippet"]["description"],
        duration_s=parse_iso8601_duration(info["contentDetails"]["duration"]),
        view_count=info["statistics"].get("viewCount", 0),
        comment_count=info["statistics"].get("commentCount", 0),
        like_count=info["statistics"].get("likeCount", 0),
    )


def parse_iso8601_duration(duration: str) -> int:
    pattern = re.compile(
        r"PT"
        r"(?:(?P<hours>\d+)H)?"
        r"(?:(?P<minutes>\d+)M)?"
        r"(?:(?P<seconds>\d+)S)?"
    )
    if match := pattern.fullmatch(duration):
        parts = {k: int(v) if v else 0 for k, v in match.groupdict().items()}
        return parts["hours"] * 3600 + parts["minutes"] * 60 + parts["seconds"]
    raise ValueError(f"Invalid ISO 8601 duration: {duration}")


@cache(expire=timedelta(hours=12), tag="youtube-info")
def fetch_youtube_info(youtube_url: str) -> YouTubeInfo:
    youtube_id = parse_youtube_id(youtube_url)
    client = google_api.get_client("youtube", "v3")
    response = (
        client.videos()
        .list(
            part="snippet,contentDetails,statistics",
            id=youtube_id,
            maxResults=1,
        )
        .execute()
    )
    if not response["items"]:
        raise ValueError(f"Video {youtube_url} not found")

    return response["items"][0]
