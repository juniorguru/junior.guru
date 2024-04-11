from pprint import pformat

from jg.core.cli.sync import main as cli
from jg.core.lib import discord_task, loggers
from jg.core.models.base import db
from jg.core.models.club import ClubMessage, ClubPin, ClubUser
from jg.core.sync.club_content.crawler import crawl


logger = loggers.from_path(__file__)


@cli.sync_command()
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
