import asyncio
import itertools
from datetime import timedelta
from pprint import pformat

import arrow
import click
from peewee import OperationalError

from juniorguru.cli.sync import main as cli, default_from_env
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (DEFAULT_CHANNELS_HISTORY_SINCE, ClubChannel,
                                         ClubEmoji, ClubMember, emoji_name,
                                         fetch_messages, fetch_threads, get_roles,
                                         is_thread_after)
from juniorguru.lib.discord_votes import count_downvotes, count_upvotes
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubPinReaction, ClubUser


logger = loggers.from_path(__file__)


WORKERS_COUNT = 5

CHANNELS_HISTORY_SINCE = {
    ClubChannel.FUN: timedelta(days=30),  # volná-zábava
    ClubChannel.FUN_TOPICS: timedelta(days=30),  # volná-témata

    # take all history since ever
    ClubChannel.INTRO: None,

    # skip channels
    ClubChannel.BOT: timedelta(0),
    ClubChannel.JOBS: timedelta(0),
    834443926655598592: timedelta(0),  # práce-bot (archived)
}


@cli.sync_command()
@click.option('--confirm/--no-confirm', default=default_from_env('CLUB_CONTENT_CONFIRM', type=bool))
def main(confirm):
    total_messages_count = get_total_messages_count()
    logger.info(f"Found {total_messages_count} messages")
    if total_messages_count:
        try:
            logger.info(f"Last message is from {get_last_message().created_at.isoformat()}")
            if not confirm or confirm_fetch():
                fetch_club_content()
        except OperationalError as e:
            logger.error(e)
            fetch_club_content()
    else:
        fetch_club_content()
    logger.info(f'Finished with\n{pformat(get_stats())}')


@db.connection_context()
def get_total_messages_count():
    try:
        return ClubMessage.count()
    except OperationalError:
        return 0


@db.connection_context()
def get_last_message():
    return ClubMessage.last_message()


def confirm_fetch():
    print('\a', end='', flush=True)
    return click.confirm('Fetch the latest club content?',
                         default=True,
                         show_default=True,
                         prompt_suffix='')


def fetch_club_content():
    with db.connection_context():
        db.drop_tables([ClubMessage, ClubUser, ClubPinReaction])
        db.create_tables([ClubMessage, ClubUser, ClubPinReaction])
    discord_sync.run(process_club_content)


@db.connection_context()
def get_stats():
    return dict(messages=ClubMessage.count(),
                users=ClubUser.count(),
                members=ClubUser.members_count(),
                pins=ClubPinReaction.count())


@db.connection_context()
async def process_club_content(client):
    channels = (channel for channel  # or just club_guild.channels ???
                in itertools.chain(client.club_guild.text_channels,
                                   client.club_guild.voice_channels,
                                   # TODO client.club_guild.stage_channels,
                                   client.club_guild.forum_channels)
                if channel.permissions_for(client.club_guild.me).read_messages)

    authors = {}

    queue = asyncio.Queue()
    for channel in channels:
        queue.put_nowait(channel)

    workers = [asyncio.create_task(channel_worker(worker_no, authors, queue))
               for worker_no in range(WORKERS_COUNT)]

    # trick to prevent hangs if workers raise, see https://stackoverflow.com/a/60710981/325365
    queue_completed = asyncio.create_task(queue.join())
    await asyncio.wait([queue_completed, *workers], return_when=asyncio.FIRST_COMPLETED)

    # if there's a worker which raised
    if not queue_completed.done():
        workers_done = [worker for worker in workers if worker.done()]
        logger.warning(f'Some workers ({len(workers_done)} of {WORKERS_COUNT}) finished before the queue is done!')
        workers_done[0].result()  # raises

    # cancel workers which are still runnning
    for worker in workers:
        worker.cancel()

    # return_exceptions=True silently collects CancelledError() exceptions
    await asyncio.gather(*workers, return_exceptions=True)

    logger_u = logger['users']
    logger_u.info('Looking for members without a single message')
    remaining_members = [member async for member
                         in client.club_guild.fetch_members(limit=None)
                         if member.id not in authors]

    logger_u.info(f'There are {len(remaining_members)} remaining members')
    for member in remaining_members:
        logger_u.debug(f"Member '{member.display_name}' #{member.id}")
        ClubUser.create(id=member.id,
                        is_bot=member.bot,
                        is_member=True,
                        has_avatar=bool(member.avatar),
                        display_name=member.display_name,
                        mention=member.mention,
                        tag=f'{member.name}#{member.discriminator}',
                        joined_at=arrow.get(member.joined_at).naive,
                        initial_roles=get_roles(member))


async def channel_worker(worker_no, authors, queue):
    logger_w = logger[f'channel_workers.{worker_no}']
    while True:
        channel = await queue.get()
        parent_channel_id = channel.parent.id if hasattr(channel, 'parent') else channel.id

        history_since = CHANNELS_HISTORY_SINCE.get(parent_channel_id, DEFAULT_CHANNELS_HISTORY_SINCE)
        if history_since is None:
            history_after = None
            logger_w.info(f"Reading channel #{channel.id} history since ever")
        else:
            history_after = (arrow.utcnow() - history_since).datetime
            logger_w.info(f"Reading channel #{channel.id} history after {history_after:%Y-%m-%d} ({history_since.days} days ago)")
        logger_w.debug(f"Channel #{channel.id} is named '{channel.name}'")

        threads = [thread async for thread in fetch_threads(channel)
                   if is_thread_after(thread, after=history_after)]
        if threads:
            logger_w.info(f"Channel #{channel.id} adds {len(threads)} threads")
        for thread in threads:
            logger_w.debug(f"Thread '{thread.name}' #{thread.id} {thread.jump_url}")
            queue.put_nowait(thread)

        messages_count = 0
        users_count = 0
        pins_count = 0
        async for message in fetch_messages(channel, after=history_after):
            if message.author.id not in authors:
                authors[message.author.id] = create_user(message.author)
                users_count += 1

            ClubMessage.create(id=message.id,
                               url=message.jump_url,
                               content=message.content,
                               content_size=len(message.content or ''),
                               reactions={emoji_name(reaction.emoji): reaction.count for reaction in message.reactions},
                               upvotes_count=count_upvotes(message.reactions),
                               downvotes_count=count_downvotes(message.reactions),
                               created_at=arrow.get(message.created_at).naive,
                               created_month=f'{message.created_at:%Y-%m}',
                               edited_at=(arrow.get(message.edited_at).naive if message.edited_at else None),
                               author=authors[message.author.id],
                               author_is_bot=message.author.id == ClubMember.BOT,
                               channel_id=channel.id,
                               channel_name=channel.name,
                               parent_channel_id=parent_channel_id,
                               category_id=channel.category_id,
                               type=message.type.name)
            messages_count += 1

            async for reacting_member in fetch_members_reacting_by_pin(message.reactions):
                if reacting_member.id not in authors:
                    authors[reacting_member.id] = create_user(reacting_member)
                    users_count += 1
                logger_w['pins'].debug(f"Message {message.jump_url} is pinned by member '{reacting_member.display_name}' #{reacting_member.id}")
                ClubPinReaction.create(member=reacting_member.id, message=message.id)
                pins_count += 1

        logger_w.info(f"Channel #{channel.id} added {messages_count} messages, {users_count} users, {pins_count} pins")
        queue.task_done()


async def fetch_members_reacting_by_pin(reactions):
    for reaction in reactions:
        if emoji_name(reaction.emoji) == ClubEmoji.PIN:
            async for user in reaction.users():
                if getattr(user, 'joined_at', False):
                    yield user


def create_user(user):
    logger['users'].debug(f"User '{user.display_name}' #{user.id}")

    # The message.author can be an instance of Member, but it can also be an instance of User,
    # if the author isn't a member of the Discord guild/server anymore. User instances don't
    # have certain properties, hence the getattr() calls below.
    return ClubUser.create(id=user.id,
                           is_bot=user.bot,
                           is_member=bool(getattr(user, 'joined_at', False)),
                           has_avatar=bool(user.avatar),
                           display_name=user.display_name,
                           mention=user.mention,
                           tag=f'{user.name}#{user.discriminator}',
                           joined_at=(arrow.get(user.joined_at).naive if hasattr(user, 'joined_at') else None),
                           initial_roles=get_roles(user))
