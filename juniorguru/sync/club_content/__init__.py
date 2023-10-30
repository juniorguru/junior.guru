from pprint import pformat

import click
from peewee import OperationalError

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubPin, ClubUser
from juniorguru.sync.club_content.crawler import crawl


logger = loggers.from_path(__file__)


@cli.sync_command()
@cli.pass_cache
@click.option('--clear-stats-cache/--keep-stats-cache', default=False)
def main(cache, clear_stats_cache):
    if clear_stats_cache:
        cache.delete('club_content_stats')
    try:
        stats = get_stats()
        logger.info(f"Found {pformat(get_stats())}")
    except OperationalError as e:
        logger.error(e)
        fetch_club_content()
    else:
        try:
            cached_stats = cache['club_content_stats']
        except KeyError:
            logger.info('No cached stats, refetching')
            fetch_club_content()
        else:
            if cached_stats != stats:
                logger.info('Data changed, refetching')
                fetch_club_content()
            else:
                logger.info('Re-using data')

    stats = get_stats()
    cache['club_content_stats'] = stats
    logger.info(f"Finished with {pformat(get_stats())}")


def fetch_club_content():
    with db.connection_context():
        db.drop_tables([ClubMessage, ClubUser, ClubPin])
        db.create_tables([ClubMessage, ClubUser, ClubPin])
    discord_sync.run(crawl)


@db.connection_context()
def get_stats() -> dict[str, int]:
    return dict(
        messages=ClubMessage.count(),
        users=ClubUser.count(),
        members=ClubUser.members_count(),
        pins=ClubPin.count(),
    )
