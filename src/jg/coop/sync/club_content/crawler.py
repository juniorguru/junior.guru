import asyncio
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

from discord import ChannelType, DMChannel, Member, Message, Reaction, User
from discord.abc import GuildChannel

from jg.coop.lib import loggers
from jg.coop.lib.discord_club import (
    DEFAULT_CHANNELS_HISTORY_SINCE,
    ClubChannelID,
    ClubClient,
    ClubEmoji,
    emoji_name,
    fetch_threads,
    get_channel_name,
    get_or_create_dm_channel,
    get_parent_channel,
    is_member,
)
from jg.coop.sync.club_content.store import (
    store_channel,
    store_dm_channel,
    store_member,
    store_message,
    store_pin,
    store_thread,
)


logger = loggers.from_path(__file__)


WORKERS_COUNT = 6

CHANNELS_HISTORY_SINCE = {
    ClubChannelID.FUN: timedelta(days=30),
    ClubChannelID.FUN_TOPICS: timedelta(days=30),
    ClubChannelID.JOBS: timedelta(days=60),
    # all history since ever
    ClubChannelID.ANNOUNCEMENTS: None,
    ClubChannelID.INTRO: None,
    ClubChannelID.BUSINESS: None,
}

CATEGORIES_SKIP = [
    1186355795311480852,  # English
    878944218545025034,  # archive
    806097273536512010,  # CoreSkill
    1005416455107526666,  # CoreSkill
    1273972027132350569,  # DP
]

CHANNELS_SKIP = [
    ClubChannelID.MODERATION,
    ClubChannelID.BOT,
    ClubChannelID.BOT_FORUM,
    ClubChannelID.JOBS_TRASH,
]


async def crawl(client: ClubClient) -> None:
    logger.info("Crawling members")
    members = []
    tasks = []
    async for member in client.club_guild.fetch_members(limit=None):
        members.append(member)
        tasks.append(asyncio.create_task(store_member(member)))
    await asyncio.gather(*tasks)

    logger.info("Crawling club channels")
    queue = asyncio.Queue()
    for channel in client.club_guild.channels:
        if channel.type == ChannelType.category:
            continue
        if channel.permissions_for(client.club_guild.me).read_messages:
            if (
                channel.id not in CHANNELS_SKIP
                and channel.category_id not in CATEGORIES_SKIP
            ):
                queue.put_nowait(channel)
            else:
                logger.debug(
                    f"Skipping channel #{channel.id} {get_channel_name(channel)!r}"
                )

    workers = [
        asyncio.create_task(channel_worker(worker_no, queue))
        for worker_no in range(WORKERS_COUNT)
    ]

    logger.info("Adding DM channels")
    dm_tasks = [
        asyncio.create_task(crawl_dm_channel(queue, member)) for member in members
    ]

    # trick to prevent hangs if workers raise, see https://stackoverflow.com/a/60710981/325365
    queue_completed = asyncio.create_task(queue.join())
    await asyncio.wait([queue_completed, *workers], return_when=asyncio.FIRST_COMPLETED)

    # if there's a worker which raised
    if not queue_completed.done():
        workers_done = [worker for worker in workers if worker.done()]
        logger.warning(
            f"Some workers ({len(workers_done)} of {WORKERS_COUNT}) finished before the queue is done!"
        )
        workers_done[0].result()  # raises

    # cancel workers which are still runnning
    for worker in workers:
        worker.cancel()

    # return_exceptions=True silently collects CancelledError() exceptions
    await asyncio.gather(*dm_tasks, *workers, return_exceptions=True)


async def crawl_dm_channel(queue: asyncio.Queue, member: Member) -> None:
    channel: DMChannel = await get_or_create_dm_channel(member)
    if channel:
        logger["channels"].debug(
            f"Adding DM channel #{channel.id} for member {channel.recipient.display_name!r}"
        )
        queue.put_nowait(channel)
        await store_dm_channel(channel)


async def channel_worker(worker_no, queue) -> None:
    logger_cw = logger[worker_no]["channels"]
    while True:
        channel: GuildChannel = await queue.get()
        logger_c = get_channel_logger(logger_cw, channel)
        logger_c.info(f"Crawling {get_channel_name(channel)!r}")
        is_thread = channel.type == ChannelType.public_thread

        # Determine how far back to crawl the channel history
        if hasattr(channel, "is_pinned") and channel.is_pinned():
            history_after = None
            logger_c.debug("Crawling all channel history (pinned forum thread)")
        else:
            history_since = CHANNELS_HISTORY_SINCE.get(
                get_parent_channel(channel).id, DEFAULT_CHANNELS_HISTORY_SINCE
            )
            if history_since is None:
                history_after = None
                logger_c.debug("Crawling all channel history")
            else:
                history_after = get_history_after(history_since)
                logger_c.debug(
                    f"Crawling history after {history_after:%Y-%m-%d} ({history_since.days} days ago)"
                )

        # Crawl the channel or decide on skipping it
        tasks = []
        messages_count = 0
        async for message in fetch_messages(channel, history_after):
            db_message = await store_message(message)
            async for reacting_member in fetch_members_reacting_by_pin(
                message.reactions
            ):
                tasks.append(
                    asyncio.create_task(store_pin(db_message, reacting_member))
                )
            messages_count += 1
        logger_c.debug(f"Stored {messages_count} messages")

        if is_thread and not messages_count:
            # Skip empty threads
            logger_c.debug(
                f"Skipping {get_channel_name(channel)!r} (no recent messages)"
            )
        else:
            if is_thread:
                # Threads cannot have threads, so just store it
                thread_members = await channel.fetch_members()
                tasks.append(asyncio.create_task(store_thread(channel, thread_members)))
            else:
                # Enqueue threads if any
                threads = [
                    thread
                    async for thread in fetch_threads(channel)
                    if not thread.is_private()
                ]
                if threads:
                    logger_c.info(f"Adding {len(threads)} threads")
                for thread in threads:
                    logger_c.debug(
                        f"Adding thread '{thread.name}' #{thread.id} {thread.jump_url}"
                    )
                    queue.put_nowait(thread)
                # Store the channel itself
                tasks.append(asyncio.create_task(store_channel(channel)))

            await asyncio.gather(*tasks)
            logger_c.debug(f"Done crawling {get_channel_name(channel)!r}")

        # Mark the channel as done
        queue.task_done()


def get_channel_logger(
    logger: loggers.Logger, channel: GuildChannel | DMChannel
) -> loggers.Logger:
    parent_channel_id = get_parent_channel(channel).id
    logger = logger[parent_channel_id]
    if parent_channel_id != channel.id:
        logger = logger[channel.id]
    return logger


async def fetch_messages(
    channel: GuildChannel | DMChannel,
    after: datetime | None,
) -> AsyncGenerator[Message, None]:
    logger_m = logger["messages"][channel.id]

    # Get channel history iterator
    try:
        channel_history = channel.history(limit=None, after=after, oldest_first=False)
    except AttributeError:
        logger_m.debug(f"Channel doesn't support history: {channel.type}")
        return

    # Iterate over messages
    count = 0
    async for message in channel_history:
        yield message
        count += 1
    logger_m.debug(f"Downloaded {count} messages")


async def fetch_members_reacting_by_pin(
    reactions: list[Reaction],
) -> AsyncGenerator[User | Member, None]:
    for reaction in reactions:
        if emoji_name(reaction.emoji) == ClubEmoji.PIN:
            async for user in reaction.users():
                if is_member(user):
                    yield user
            break


def get_history_after(
    history_since: timedelta | None, now: datetime = None
) -> datetime:
    if now:
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
    else:
        now = datetime.now(timezone.utc)
    return now - history_since
