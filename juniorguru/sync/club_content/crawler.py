import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from functools import partial
from operator import itemgetter
import random
from typing import Generator

from discord import DMChannel, Member, Message, Reaction, User
from discord.state import ConnectionState
from discord.types.message import Message as MessagePayload
from discord.abc import GuildChannel
from discord.utils import time_snowflake

from juniorguru.lib import loggers
from juniorguru.lib.cache import get_cache, _call_async
from juniorguru.lib.discord_club import (
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
    is_thread_after,
)
from juniorguru.sync.club_content.store import (
    store_dm_channel,
    store_member,
    store_message,
    store_pin,
)


logger = loggers.from_path(__file__)


WORKERS_COUNT = 6

CHANNELS_HISTORY_SINCE = {
    ClubChannelID.FUN: timedelta(days=30),
    ClubChannelID.FUN_TOPICS: timedelta(days=30),
    ClubChannelID.INTRO: None,  # all history since ever
    ClubChannelID.BUSINESS: None,  # all history since ever
    ClubChannelID.MENTORING: None,  # all history since ever
}

CHANNELS_SKIP = [
    # skip channels
    ClubChannelID.MODERATION,
    ClubChannelID.BOT,
    ClubChannelID.JOBS,
    # skip práce-bot (archived)
    834443926655598592,
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
        if (
            channel.type != "category"
            and channel.permissions_for(client.club_guild.me).read_messages
        ):
            if channel.id not in CHANNELS_SKIP:
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
    channel = await get_or_create_dm_channel(member)
    if channel:
        logger["channels"].debug(
            f"Adding DM channel #{channel.id} for member {channel.recipient.display_name!r}"
        )
        queue.put_nowait(channel)
        await store_dm_channel(channel)


async def channel_worker(worker_no, queue) -> None:
    logger_cw = logger[worker_no]["channels"]
    while True:
        channel = await queue.get()
        logger_c = get_channel_logger(logger_cw, channel)
        logger_c.info(f"Crawling {get_channel_name(channel)!r}")

        cache_cutoff_at = datetime.now(timezone.utc) - timedelta(days=20)
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

        threads = [
            thread
            async for thread in fetch_threads(channel)
            if is_thread_after(thread, after=history_after) and not thread.is_private()
        ]
        if threads:
            logger_c.info(f"Adding {len(threads)} threads")
        for thread in threads:
            logger_c.debug(
                f"Adding thread '{thread.name}' #{thread.id} {thread.jump_url}"
            )
            queue.put_nowait(thread)

        tasks = []
        async for message in fetch_messages(channel, history_after, cache_cutoff_at):
            db_message = await store_message(message)
            async for reacting_member in fetch_members_reacting_by_pin(
                message.reactions
            ):
                tasks.append(
                    asyncio.create_task(store_pin(db_message, reacting_member))
                )
        await asyncio.gather(*tasks)

        logger_c.debug(f"Done crawling {get_channel_name(channel)!r}")
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
    cache_cutoff_at: datetime,
    payloads_expire_days=5,
    payloads_expire_randomness=10,
) -> Generator[Message, None, None]:
    logger_m = logger["messages"][channel.id]

    # Get channel history iterator
    try:
        channel_history = channel.history
    except AttributeError:
        logger_m.debug(f"Channel doesn't support history: {channel.type}")
        return
    iterator = channel_history(limit=None, after=after, oldest_first=False)

    # Load cached messages
    cache = get_cache()
    cache_key = f"message-payloads:{channel.id}"

    payloads_mapping: dict[int, MessagePayload] = await _call_async(
        cache.get, cache_key, {}
    )
    payloads = filter_payloads(payloads_mapping.values(), after, cache_cutoff_at)
    cached_ids = frozenset(int(payload["id"]) for payload in payloads)

    # Detect if we can read the whole channel from cache
    if getattr(channel, "last_message_id", None) in cached_ids:
        logger_m.debug("Reading whole channel from cache")
        for payload in payloads:
            yield await _call_async(create_message, iterator.state, channel, payload)
        return

    # Patch the iterator to collect payloads
    _retrieve_messages = iterator._retrieve_messages

    async def _retrieve_messages_patched(*args, **kwargs) -> list[MessagePayload]:
        payloads_batch = list(await _retrieve_messages(*args, **kwargs))
        payloads_mapping.update(
            {int(payload["id"]): deepcopy(payload) for payload in payloads_batch}
        )
        return payloads_batch

    iterator._retrieve_messages = _retrieve_messages_patched

    # Iterate over messages
    count_downloaded = 0
    count_cached = 0
    async for message in iterator:
        if message.id in cached_ids:
            for payload in payloads:
                yield await _call_async(
                    create_message, iterator.state, channel, payload
                )
                count_cached += 1
            break
        else:
            yield message
            count_downloaded += 1
    logger_m.debug(
        f"Downloaded {count_downloaded} messages, "
        f"loaded {count_cached} messages from cache, "
        f"total {count_downloaded + count_cached} messages"
    )

    if payloads_mapping:
        # Store payloads, but only for a limited time - this is again, to allow
        # for updates like edits and deletes to propagate to the cache.
        # The randomness is to prevent all messages from expiring at the same time,
        # instead to gradually expire channels and renew their cache over the course
        # of a few days.
        days = payloads_expire_days + random.randint(0, payloads_expire_randomness)
        logger_m.debug(f"Caching {len(payloads_mapping)} messages for {days} days")
        await _call_async(
            cache.set,
            cache_key,
            payloads_mapping,
            timedelta(days=days).total_seconds(),
            tag="messages",
        )


def filter_payloads(
    payloads: list[MessagePayload],
    after: datetime | None,
    before: datetime | None,
) -> list[MessagePayload]:
    if after:
        payloads = filter(partial(is_payload_after, after=after), payloads)
    if before:
        payloads = filter(partial(is_payload_before, before=before), payloads)
    return sorted(payloads, key=itemgetter("id"), reverse=True)


def is_payload_after(payload: MessagePayload, after: datetime) -> bool:
    return int(payload["id"]) > time_snowflake(after, high=True)


def is_payload_before(payload: MessagePayload, before: datetime) -> bool:
    return int(payload["id"]) < time_snowflake(before, high=False)


def is_message_before(message: Message, before: datetime) -> bool:
    return message.id < time_snowflake(before, high=False)


def is_channel_before(channel: GuildChannel | DMChannel, before: datetime) -> bool:
    if getattr(channel, "last_message_id", None) is None:
        return False
    return channel.last_message_id < time_snowflake(before, high=False)


def create_message(
    state: ConnectionState, channel: GuildChannel | DMChannel, data: MessagePayload
) -> Message:
    return state.create_message(channel=channel, data=deepcopy(data))


async def fetch_members_reacting_by_pin(
    reactions: list[Reaction],
) -> Generator[User | Member, None, None]:
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
