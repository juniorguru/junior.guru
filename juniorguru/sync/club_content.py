import asyncio
import itertools
import os
from datetime import datetime, timezone

import arrow
import click
from peewee import OperationalError

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import (CHANNELS_HISTORY_SINCE, DEFAULT_CHANNELS_HISTORY_SINCE,
                                 EMOJI_PIN, count_downvotes, count_upvotes, emoji_name,
                                 get_roles, run_discord_task)
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubPinReaction, ClubUser


logger = loggers.from_path(__file__)


WORKERS_COUNT = 5

DEFAULT_CREATED_AT = datetime(2022, 1, 9, tzinfo=timezone.utc)  # threads have 'created_at' since 2022-01-09


@cli.sync_command()
@click.option('--confirm/--no-confirm', default=lambda: bool(os.environ.get('CLUB_CONTENT_CONFIRM', '')))
def main(confirm):
    total_messages_count = get_total_messages_count()
    logger.info(f"Found {total_messages_count} messages")
    if total_messages_count:
        try:
            logger.info(f"Last message is from {get_last_message().created_at.isoformat()}")
            if not confirm or confirm_fetch():
                run_discord_task('juniorguru.sync.club_content.discord_task')
        except OperationalError as e:
            logger.error(e)
            run_discord_task('juniorguru.sync.club_content.discord_task')
    else:
        run_discord_task('juniorguru.sync.club_content.discord_task')

    with db.connection_context():
        logger.info(f'Finished with {ClubMessage.count()} messages, '
                    f'{ClubUser.members_count()} users, '
                    f'{ClubPinReaction.count()} pins')


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


@db.connection_context()
async def discord_task(client):
    db.drop_tables([ClubMessage, ClubUser, ClubPinReaction])
    db.create_tables([ClubMessage, ClubUser, ClubPinReaction])

    channels = (channel for channel
                in itertools.chain(client.juniorguru_guild.text_channels,
                                   client.juniorguru_guild.voice_channels,
                                   client.juniorguru_guild.forum_channels)
                if channel.permissions_for(client.juniorguru_guild.me).read_messages)
    authors = await process_channels(channels)

    logger_u = logger['users']
    logger_u.info('Looking for members without a single message')
    remaining_members = [member async for member
                         in client.juniorguru_guild.fetch_members(limit=None)
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


async def process_channels(channels):
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

    return authors


async def channel_worker(worker_no, authors, queue):
    logger_w = logger[f'channel_workers.{worker_no}']
    while True:
        channel = await queue.get()

        history_since = CHANNELS_HISTORY_SINCE.get(channel.id, DEFAULT_CHANNELS_HISTORY_SINCE)
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
                               content_size=len(message.content),
                               reactions={emoji_name(reaction.emoji): reaction.count for reaction in message.reactions},
                               upvotes_count=count_upvotes(message.reactions),
                               downvotes_count=count_downvotes(message.reactions),
                               created_at=arrow.get(message.created_at).naive,
                               created_month=f'{message.created_at:%Y-%m}',
                               edited_at=(arrow.get(message.edited_at).naive if message.edited_at else None),
                               author=authors[message.author.id],
                               channel_id=channel.id,
                               channel_name=channel.name,
                               channel_mention=channel.mention,
                               type=message.type.name)
            messages_count += 1

            async for reacting_user in fetch_users_reacting_by_pin(message.reactions):
                if reacting_user.id not in authors:
                    authors[reacting_user.id] = create_user(reacting_user)
                    users_count += 1
                logger_w['pins'].debug(f"Message {message.jump_url} is pinned by user '{reacting_user.display_name}' #{reacting_user.id}")
                ClubPinReaction.create(user=reacting_user.id, message=message.id)
                pins_count += 1

        logger_w.info(f"Channel #{channel.id} added {messages_count} messages, {users_count} users, {pins_count} pins")
        queue.task_done()


async def fetch_messages(channel, after=None):
    try:
        channel_history = channel.history
    except AttributeError:
        pass  # channel type doesn't support history (e.g. forum)
    else:
        async for message in channel_history(limit=None, after=after):
            yield message


async def fetch_threads(channel):
    try:
        channel_threads = channel.threads
    except AttributeError:
        pass  # channel type doesn't support threads (e.g. voice)
    else:
        for thread in channel_threads:
            yield thread
        async for thread in channel.archived_threads(limit=None):
            yield thread


def is_thread_after(thread, after=None):
    if after:
        return (thread.created_at or DEFAULT_CREATED_AT) >= after
    return thread


async def fetch_users_reacting_by_pin(reactions):
    for reaction in reactions:
        if emoji_name(reaction.emoji) == EMOJI_PIN:
            async for user in reaction.users():
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
