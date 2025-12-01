import peewee
from discord import DMChannel, Member, Message, Thread, ThreadMember, User
from discord.abc import GuildChannel

from jg.coop.lib import loggers
from jg.coop.lib.async_utils import make_async
from jg.coop.lib.discord_club import (
    ClubMemberID,
    emoji_name,
    get_channel_name,
    get_parent_channel,
    get_pinned_message_url,
    get_starting_emoji,
    get_ui_urls,
    get_user_roles,
    is_channel_private,
    is_forum_guide,
)
from jg.coop.lib.discord_votes import count_downvotes, count_upvotes
from jg.coop.models.base import db
from jg.coop.models.club import ClubChannel, ClubMessage, ClubPin, ClubUser


logger = loggers.from_path(__file__)


@make_async
@db.connection_context()
def store_member(member: Member) -> ClubUser:
    """Stores in database given Discord Member object"""
    logger["users"][member.id].debug(f"Saving {member.display_name!r}")
    return ClubUser.create(
        id=member.id,
        is_bot=member.bot,
        is_member=True,
        has_avatar=bool(member.avatar),
        display_name=member.display_name,
        mention=member.mention,
        joined_at=member.joined_at.replace(tzinfo=None),
        initial_roles=get_user_roles(member),
    )


@db.connection_context()
def _store_user(user: User) -> ClubUser:
    """
    Stores in database given Discord User object

    If given user is already stored, it silently returns the existing database object.
    """
    logger["users"][user.id].debug(f"Saving {user.display_name!r}")
    try:
        # The message.author can be an instance of Member, but it can also be an instance of User,
        # if the author isn't a member of the Discord guild/server anymore. User instances don't
        # have certain properties, hence the getattr() calls below.
        obj = ClubUser.create(
            id=user.id,
            is_bot=user.bot,
            is_member=bool(getattr(user, "joined_at", False)),
            has_avatar=bool(user.avatar),
            display_name=user.display_name,
            mention=user.mention,
            joined_at=(
                user.joined_at.replace(tzinfo=None)
                if hasattr(user, "joined_at")
                else None
            ),
            initial_roles=get_user_roles(user),
        )
        logger["users"][user.id].debug(f"Saved {user.display_name!r} as {obj!r}")
        return obj
    except peewee.IntegrityError:
        obj = ClubUser.get_by_id(user.id)
        logger["users"][user.id].debug(f"Found {user.display_name!r} as {obj!r}")
        return obj


@make_async
@db.connection_context()
def store_message(message: Message) -> ClubMessage:
    """
    Stores in database given Discord Message object

    If the author isn't stored yet, it stores it along the way.
    """
    # The channel can be a GuildChannel, but it can also be a DMChannel.
    # Those have different properties, hence the get_...() and getattr() calls below.
    channel = message.channel
    try:
        return ClubMessage.create(
            id=message.id,
            url=message.jump_url,
            content=message.content,
            content_size=len(message.content or ""),
            content_starting_emoji=get_starting_emoji(message.content),
            reactions={
                emoji_name(reaction.emoji): reaction.count
                for reaction in message.reactions
            },
            upvotes_count=count_upvotes(message.reactions),
            downvotes_count=count_downvotes(message.reactions),
            created_at=message.created_at.replace(tzinfo=None),
            created_month=f"{message.created_at:%Y-%m}",
            edited_at=(
                message.edited_at.replace(tzinfo=None) if message.edited_at else None
            ),
            author=_store_user(message.author),
            author_is_bot=message.author.id == ClubMemberID.BOT,
            channel_id=channel.id,
            channel_name=get_channel_name(channel),
            channel_type=int(channel.type.value),
            parent_channel_id=get_parent_channel(channel).id,
            parent_channel_name=get_channel_name(get_parent_channel(channel)),
            parent_channel_type=int(get_parent_channel(channel).type.value),
            category_id=getattr(channel, "category_id", None),
            type=message.type.name,
            is_private=is_channel_private(channel),
            pinned_message_url=get_pinned_message_url(message),
            ui_urls=get_ui_urls(message),
            is_forum_guide=is_forum_guide(message),
        )
    except peewee.IntegrityError:
        message_obj = ClubMessage.get_by_id(message.id)
        logger["messages"].debug(
            f"Message {message.jump_url} apparently already stored as {message_obj!r}"
        )
        return message_obj


@make_async
@db.connection_context()
def store_pin(message: ClubMessage, member: Member) -> None:
    """
    Stores in database the information about given Discord Member pinning given Discord Message

    If the reacting member isn't stored yet, it stores it along the way.
    """
    logger["pins"].debug(
        f"Message {message.url} is pinned by member '{member.display_name}' #{member.id}"
    )
    ClubPin.create(
        pinned_message=message.id, member=ClubUser.get_member_by_id(member.id)
    )


@make_async
@db.connection_context()
def store_thread(thread: Thread, members: list[ThreadMember]) -> None:
    """Stores in database the information about given Discord public thread"""
    name = get_channel_name(thread)
    logger["channels"].debug(f"Thread #{thread.id} aka {name!r}")
    ClubChannel.create(
        id=thread.id,
        name=name,
        type=int(thread.type.value),
        tags=[tag.name for tag in thread.applied_tags],
        author_id=thread.owner_id,
        members_ids=[member.id for member in members if member.id != ClubMemberID.BOT],
    )


@make_async
@db.connection_context()
def store_channel(channel: GuildChannel) -> None:
    """Stores in database the information about given Discord channel"""
    name = get_channel_name(channel)
    logger["channels"].debug(
        f"Channel #{channel.id} aka {name!r}, type {channel.type.name}"
    )
    ClubChannel.create(id=channel.id, name=name, type=int(channel.type.value))


@make_async
@db.connection_context()
def store_dm_channel(channel: DMChannel) -> None:
    """Stores in database the information about given Discord DM channel"""
    # Assuming the recipient is a member, but also ensuring it REALLY IS a member
    # in the where() clause below.
    member = channel.recipient
    logger["dm"].debug(
        f"Channel {channel.id} belongs to member '{member.display_name}' #{member.id}"
    )
    rows_count = (
        ClubUser.update({ClubUser.dm_channel_id: channel.id})
        .where(ClubUser.id == member.id, ClubUser.is_member == True)  # noqa: E712
        .execute()
    )
    if rows_count != 1:
        raise RuntimeError(
            f"Unexpected number of rows updated ({rows_count}) when recording DM channel #{channel.id} to member #{member.id}"
        )
