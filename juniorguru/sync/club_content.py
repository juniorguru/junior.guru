import asyncio
from datetime import timedelta

import arrow

from juniorguru.lib import loggers
from juniorguru.lib.club import (EMOJI_PINS, count_downvotes, count_pins, count_upvotes,
                                 emoji_name, get_roles, run_discord_task, FUN_CHANNEL,
                                 INTRO_CHANNEL, BOT_CHANNEL)
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubPinReaction, ClubUser


logger = loggers.get(__name__)


WORKERS_COUNT = 5

DEFAULT_CHANNELS_HISTORY_SINCE = timedelta(days=380)

CHANNELS_HISTORY_SINCE = {
    FUN_CHANNEL: timedelta(days=30),
    INTRO_CHANNEL: None,  # means 'take all history since ever'
    BOT_CHANNEL: timedelta(0),  # means 'skip the channel'
}


@sync_task()
def main():
    run_discord_task('juniorguru.sync.club_content.discord_task')


@db.connection_context()
async def discord_task(client):
    db.drop_tables([ClubMessage, ClubUser, ClubPinReaction])
    db.create_tables([ClubMessage, ClubUser, ClubPinReaction])

    channels = (channel for channel in client.juniorguru_guild.text_channels
                if channel.permissions_for(client.juniorguru_guild.me).read_messages)
    authors = await process_channels(channels)

    logger_u = logger.getChild('users')
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
                        roles=get_roles(member))

    logger.info(f'Created {ClubMessage.count()} messages from {len(authors)} authors, '
                f'{ClubUser.members_count()} users, '
                f'{ClubPinReaction.count()} pins')


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
        failed_workers = {worker_no: worker for worker_no, worker
                          in enumerate(workers) if worker.done()}
        logger.warning(f"Some workers (numbers: {', '.join(map(str, failed_workers.keys()))}) finished before the queue is done!")
        first_failed_worker = list(failed_workers.values())[0]
        first_failed_worker.result()  # raises

    # cancel workers which are still runnning
    for worker in workers:
        worker.cancel()

    # return_exceptions=True silently collects CancelledError() exceptions
    await asyncio.gather(*workers, return_exceptions=True)

    return authors


async def channel_worker(worker_no, authors, queue):
    logger_w = logger.getChild(f'channel_workers.{worker_no}')
    while True:
        channel = await queue.get()
        print('DBG GET CHANNEL:', repr(channel.guild), repr(channel))
        assert channel.guild, repr(channel)
        history_since = CHANNELS_HISTORY_SINCE.get(channel.id, DEFAULT_CHANNELS_HISTORY_SINCE)
        history_after = None if history_since is None else (arrow.utcnow() - history_since).datetime

        logger_w.info(f"Reading channel #{channel.id} messages after {history_after} ({history_since!r} ago)")
        logger_w.debug(f"Channel #{channel.id} is named '{channel.name}'")

        messages_count = 0
        users_count = 0
        pins_count = 0

        async for message in channel.history(limit=None, after=history_after):
            if message.thread:
                logger_w.debug(f"Thread titled '{message.thread.name}' starts from {message.jump_url}")
                print('DBG PUT THREAD:', repr(message.thread.guild), repr(message.thread))
                assert message.thread.guild, repr(message.thread)
                queue.put_nowait(message.thread)

            if message.author.id not in authors:
                authors[message.author.id] = create_user(message.author)
                users_count += 1

            ClubMessage.create(id=message.id,
                               url=message.jump_url,
                               content=message.content,
                               upvotes_count=count_upvotes(message.reactions),
                               downvotes_count=count_downvotes(message.reactions),
                               pin_reactions_count=count_pins(message.reactions),
                               created_at=arrow.get(message.created_at).naive,
                               edited_at=(arrow.get(message.edited_at).naive if message.edited_at else None),
                               author=authors[message.author.id],
                               channel_id=channel.id,
                               channel_name=channel.name,
                               channel_mention=channel.mention,
                               type=message.type.name)
            messages_count += 1

            for reacting_user in (await get_reacting_users(message.reactions)):
                if reacting_user.id not in authors:
                    authors[reacting_user.id] = create_user(reacting_user)
                    users_count += 1

                create_reaction(reacting_user, message)
                pins_count += 1

        logger_w.info(f"Channel #{channel.id} added {messages_count} messages, {users_count} users, {pins_count} pins")
        queue.task_done()


async def get_reacting_users(reactions):
    users = set()
    for reaction in reactions:
        if emoji_name(reaction.emoji) in EMOJI_PINS:
            for user in [user async for user in reaction.users()]:
                users.add(user)
    return users


def create_user(user):
    logger_u = logger.getChild('users')
    logger_u.debug(f"User '{user.display_name}' #{user.id}")

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
                           roles=get_roles(user))


def create_reaction(user, message):
    logger_p = logger.getChild('pins')
    logger_p.debug(f"Message {message.jump_url} is pinned by user '{user.display_name}' #{user.id}")
    return ClubPinReaction.create(user=user.id, message=message.id)
