import os
from pprint import pformat

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cache import cache
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage, ClubPin, ClubUser
from jg.coop.sync.club_content.crawler import crawl


logger = loggers.from_path(__file__)


@cli.sync_command()
@cache(expire=int(os.getenv("CACHE_CLUB_CONTENT", "0")), tag="club-content")
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
