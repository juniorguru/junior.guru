import asyncio
from datetime import date
from pathlib import Path
from typing import Generator, Iterable, TypedDict

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI, ButtondownError
from jg.coop.lib.cache import get_cache
from jg.coop.lib.chunks import chunks
from jg.coop.lib.cli import async_command
from jg.coop.lib.memberful import MemberfulAPI, timestamp_to_date
from jg.coop.models.base import db


MEMBERS_GQL_PATH = Path(__file__).parent / "members.gql"


logger = loggers.from_path(__file__)


class SubscriptionEntity(TypedDict):
    createdAt: int


class MemberEntity(TypedDict):
    email: str
    subscriptions: list[SubscriptionEntity]


@cli.sync_command()
@click.option("--cache-key", default="newsletter:subscribers")
@click.option("--cache-hrs", default=60, type=int)
@click.option("-f", "--force", is_flag=True, default=False)
@click.option("--chunk-size", default=3, type=int)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--recent-days", default=60, type=int)
@db.connection_context()
@async_command
async def main(
    cache_key: str,
    cache_hrs: int,
    force: bool,
    chunk_size: int,
    today: date,
    recent_days: int,
):
    cache = get_cache()
    if not force and (subscribers := cache.get(cache_key)):
        logger.info(f"Using cached {len(subscribers)} subscribers")
    else:
        subscribers = {}
        logger.info("Fetching subscribers from Memberful")
        memberful = MemberfulAPI()
        members: Generator[MemberEntity] = memberful.get_nodes(
            MEMBERS_GQL_PATH.read_text()
        )
        recently_subscribed_memebers = [
            member
            for member in members
            if (member_date := get_latest_subscription_date(member))
            and (today - member_date).days <= recent_days
        ]
        logger.info(
            f"Found {len(recently_subscribed_memebers)} members with subscriptions in the last {recent_days} days"
        )
        for member in recently_subscribed_memebers:
            subscribers.setdefault(member["email"], set())
            subscribers[member["email"]].add("memberful")
        logger.info(f"Fetched {len(subscribers)} subscribers from Memberful")
        logger.debug("Caching subscribers")
        cache.set(
            cache_key,
            subscribers,
            expire=3600 * cache_hrs,
            tag="newsletter-subscribers",
        )

    logger.info(f"Adding {len(subscribers)} subscribers to Buttondown")
    tasks = {}
    try:
        async with ButtondownAPI() as buttondown:
            for chunk in chunks(logger.progress(subscribers.items()), size=chunk_size):
                logger.debug(f"Processing chunk of {len(chunk)} subscribers")
                async with asyncio.TaskGroup() as group:
                    for email, sources in chunk:
                        tasks[email] = group.create_task(
                            buttondown.add_subscriber(email=email, tags=sources)
                        )
    except* ButtondownError as eg:
        if [e for e in eg.exceptions if e.code == "rate_limited"]:
            logger.error("Rate limited for today")
        else:
            raise


def get_latest_subscription_date(member: MemberEntity) -> date | None:
    if member["subscriptions"]:
        timestamp = max(
            subscription["createdAt"] for subscription in member["subscriptions"]
        )
        return timestamp_to_date(timestamp)
    return None
