import asyncio
import itertools
from datetime import timedelta, datetime

from juniorguru.lib import loggers
from juniorguru.lib.discord_club import (DEFAULT_CHANNELS_HISTORY_SINCE, ClubChannel,
                                         ClubEmoji, emoji_name,
                                         fetch_messages, fetch_threads,
                                         is_thread_after, get_parent_channel_id)
from juniorguru.sync.club_content.store import store_member, store_user, store_message, store_pin


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


async def crawl(client):
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
        await store_member(member)


async def channel_worker(worker_no, authors, queue):
    logger_w = logger[f'channel_workers.{worker_no}']
    while True:
        channel = await queue.get()
        parent_channel_id = get_parent_channel_id(channel)
        history_since = CHANNELS_HISTORY_SINCE.get(parent_channel_id, DEFAULT_CHANNELS_HISTORY_SINCE)
        if history_since is None:
            history_after = None
            logger_w.info(f"Reading channel #{channel.id} history since ever")
        else:
            history_after = (datetime.utcnow() - history_since).datetime
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
                authors[message.author.id] = await store_user(message.author)
                users_count += 1
            await store_message(message, channel, authors[message.author.id])
            messages_count += 1

            async for reacting_member in fetch_members_reacting_by_pin(message.reactions):
                if reacting_member.id not in authors:
                    authors[reacting_member.id] = await store_user(reacting_member)
                    users_count += 1
                await store_pin(message, reacting_member)
                pins_count += 1

        logger_w.info(f"Channel #{channel.id} added {messages_count} messages, {users_count} users, {pins_count} pins")
        queue.task_done()


async def fetch_members_reacting_by_pin(reactions):
    for reaction in reactions:
        if emoji_name(reaction.emoji) == ClubEmoji.PIN:
            async for user in reaction.users():
                if getattr(user, 'joined_at', False):
                    yield user
