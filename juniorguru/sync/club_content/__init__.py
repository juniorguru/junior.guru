from pprint import pformat

import click
from peewee import OperationalError

from juniorguru.cli.sync import confirm, default_from_env, main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubPinReaction, ClubUser
from juniorguru.sync.club_content.crawler import crawl


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--confirm/--no-confirm', 'do_confirm', default=default_from_env('CLUB_CONTENT_CONFIRM', type=bool))
def main(do_confirm):
    total_messages_count = get_total_messages_count()
    logger.info(f"Found {total_messages_count} messages")
    if total_messages_count:
        try:
            logger.info(f"Last message is from {get_last_message().created_at.isoformat()}")
            if not do_confirm or confirm('Fetch the latest club content?'):
                fetch_club_content()
        except OperationalError as e:
            logger.error(e)
            fetch_club_content()
    else:
        fetch_club_content()
    logger.info(f'Finished with {pformat(get_stats())}')


@db.connection_context()
def get_total_messages_count():
    try:
        return ClubMessage.count()
    except OperationalError:
        return 0


@db.connection_context()
def get_last_message():
    return ClubMessage.last_message()


def fetch_club_content():
    with db.connection_context():
        db.drop_tables([ClubMessage, ClubUser, ClubPinReaction])
        db.create_tables([ClubMessage, ClubUser, ClubPinReaction])
    discord_sync.run(crawl)


@db.connection_context()
def get_stats():
    return dict(messages=ClubMessage.count(),
                users=ClubUser.count(),
                members=ClubUser.members_count(),
                pins=ClubPinReaction.count())
