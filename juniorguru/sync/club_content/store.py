import asyncio
from functools import wraps, partial

import arrow

from juniorguru.models.base import db
from juniorguru.lib.discord_club import get_roles, emoji_name, ClubMember, get_parent_channel_id
from juniorguru.lib.discord_votes import count_downvotes, count_upvotes
from juniorguru.models.club import ClubMessage, ClubPinReaction, ClubUser
from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


async def make_async(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))
    return wrapper


@make_async
@db.connection_context()
def store_member(member):
    """Stores in database given Discord Member object"""
    logger['users'].debug(f"Member '{member.display_name}' #{member.id}")
    return ClubUser.create(id=member.id,
                           is_bot=member.bot,
                           is_member=True,
                           has_avatar=bool(member.avatar),
                           display_name=member.display_name,
                           mention=member.mention,
                           tag=f'{member.name}#{member.discriminator}',
                           joined_at=arrow.get(member.joined_at).naive,
                           initial_roles=get_roles(member))


@make_async
@db.connection_context()
def store_user(user):
    """
    Stores in database given Discord User object

    The message.author can be an instance of Member, but it can also be an instance of User,
    if the author isn't a member of the Discord guild/server anymore. User instances don't
    have certain properties, hence the getattr() calls.
    """
    logger['users'].debug(f"User '{user.display_name}' #{user.id}")
    return ClubUser.create(id=user.id,
                           is_bot=user.bot,
                           is_member=bool(getattr(user, 'joined_at', False)),
                           has_avatar=bool(user.avatar),
                           display_name=user.display_name,
                           mention=user.mention,
                           tag=f'{user.name}#{user.discriminator}',
                           joined_at=(arrow.get(user.joined_at).naive if hasattr(user, 'joined_at') else None),
                           initial_roles=get_roles(user))


@make_async
@db.connection_context()
def store_message(message, channel, db_author):
    """Stores in database given Discord Message object"""
    return ClubMessage.create(id=message.id,
                              url=message.jump_url,
                              content=message.content,
                              content_size=len(message.content or ''),
                              reactions={emoji_name(reaction.emoji): reaction.count for reaction in message.reactions},
                              upvotes_count=count_upvotes(message.reactions),
                              downvotes_count=count_downvotes(message.reactions),
                              created_at=arrow.get(message.created_at).naive,
                              created_month=f'{message.created_at:%Y-%m}',
                              edited_at=(arrow.get(message.edited_at).naive if message.edited_at else None),
                              author=db_author,
                              author_is_bot=message.author.id == ClubMember.BOT,
                              channel_id=channel.id,
                              channel_name=channel.name,
                              parent_channel_id=get_parent_channel_id(channel),
                              category_id=channel.category_id,
                              type=message.type.name)


@make_async
@db.connection_context()
def store_pin(message, member):
    """Stores in database the information about given Discord Member pinning given Discord Message"""
    logger['pins'].debug(f"Message {message.jump_url} is pinned by member '{member.display_name}' #{member.id}")
    return ClubPinReaction.create(member=member.id, message=message.id)
