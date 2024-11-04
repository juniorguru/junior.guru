import logging
import os
from pprint import pformat

from discord import DiscordServerError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cache import cache
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage, ClubPin, ClubUser
from jg.coop.sync.club_content.crawler import crawl


logger = loggers.from_path(__file__)


@cli.sync_command()
@cache(expire=int(os.getenv("CACHE_CLUB_CONTENT", "0")), tag="club-content")
@retry(
    retry=retry_if_exception_type(DiscordServerError),
    wait=wait_random_exponential(min=60, max=5 * 60),
    stop=stop_after_attempt(3),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def main():
    with db.connection_context():
        db.drop_tables([ClubMessage, ClubUser, ClubPin])
        db.create_tables([ClubMessage, ClubUser, ClubPin])

    discord_task.run(crawl)

    with db.connection_context():
        stats = dict(
            messages=ClubMessage.count(),
            users=ClubUser.count(),
            members=ClubUser.members_count(),
            pins=ClubPin.count(),
        )
    logger.info(f"Finished with {pformat(stats)}")
