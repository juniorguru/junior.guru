import json
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers


logger = loggers.from_path(__file__)


DATETIME_KEY = "postedAtISO"


@cli.sync_command()
@click.option("--actor", "actor_name", default="supreme_coder/linkedin-post")
@click.option(
    "--posts-dir",
    default=Path("src/jg/coop/data/posts_linkedin"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
def main(actor_name: str, posts_dir: Path) -> None:
    logger.info(f"Fetching LinkedIn posts from {actor_name}")
    posts = apify.fetch_data(actor_name)
    logger.info(f"Fetched {len(posts)} posts")

    posts_dir.mkdir(parents=True, exist_ok=True)
    for post in posts:
        filename = get_post_filename(post)
        content = serialize_post(post)

        file_path = posts_dir / filename
        file_path.write_text(content)

    logger.info(f"Saved {len(posts)} post files")


def parse_posted_at(value: str) -> datetime:
    normalized_value = str(value).strip().replace("Z", "+00:00")
    return datetime.fromisoformat(normalized_value)


def get_post_filename(post: dict) -> str:
    posted_at = parse_posted_at(post[DATETIME_KEY])
    return f"{posted_at:%Y-%m-%dT%H-%M}.json"


def serialize_post(post: dict) -> str:
    post = strip_tracking_params(post)
    post = remove_tracking_id(post)
    return json.dumps(post, ensure_ascii=False, indent=2) + "\n"


def strip_tracking_params(post: dict) -> dict:
    if not isinstance(post.get("url"), str):
        return post

    split_url = urlsplit(post["url"])
    url = urlunsplit(
        (split_url.scheme, split_url.netloc, split_url.path, "", split_url.fragment)
    )
    return {**post, "url": url}


def remove_tracking_id(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: remove_tracking_id(item)
            for key, item in value.items()
            if key != "trackingId"
        }
    if isinstance(value, list):
        return [remove_tracking_id(item) for item in value]
    return value
