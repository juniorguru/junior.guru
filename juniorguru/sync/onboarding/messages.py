import asyncio
from datetime import date
from operator import attrgetter

import discord

from juniorguru.lib import loggers
from juniorguru.lib.chunks import chunks
from juniorguru.lib.discord_club import ClubClient, get_reaction
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.sync.onboarding.scheduled_messages import (
    ALLOWED_MENTIONS,
    SCHEDULED_MESSAGES,
)


TODAY = date.today()

MEMBERS_CHUNK_SIZE = 10

EMOJI_UNREAD = "✅"


logger = loggers.from_path(__file__)


async def send_messages(client: ClubClient):
    members_chunks = chunks(ClubUser.onboarding_listing(), size=MEMBERS_CHUNK_SIZE)
    for n, members_chunk in enumerate(members_chunks, start=1):
        logger.debug(f"Processing chunk #{n} of {len(members_chunk)} members")
        await asyncio.gather(
            *[send_messages_to_member(client, member) for member in members_chunk]
        )


async def send_messages_to_member(client: ClubClient, member):
    logger_m = logger[f"members.{member.id}"]
    logger_m.debug("Preparing messages")
    messages = prepare_messages(
        ClubMessage.channel_listing_bot(member.onboarding_channel_id),
        SCHEDULED_MESSAGES,
        TODAY,
        context=dict(member=member),
    )
    if not messages:
        logger_m.debug("Nothing to do")
        return
    logger_m.info(f"Processing {len(messages)} messages")

    channel = await client.fetch_channel(member.onboarding_channel_id)
    for message_id, message_content in messages:
        if message_id:
            logger_m.debug(
                f"Editing message {message_content[0]}: {len(message_content)} characters"
            )
            discord_message = await channel.fetch_message(message_id)
            message_data = await create_message_data(client, member, message_content)
            with mutating_discord(discord_message) as proxy:
                await proxy.edit(**message_data)
            if not get_reaction(discord_message.reactions, EMOJI_UNREAD):
                with mutating_discord(discord_message) as proxy:
                    await proxy.add_reaction(EMOJI_UNREAD)
        else:
            logger_m.debug(
                f"Sending message {message_content[0]}: {len(message_content)} characters"
            )
            message_data = await create_message_data(client, member, message_content)
            with mutating_discord(channel) as proxy:
                discord_message = await proxy.send(**message_data)
            if hasattr(discord_message, "add_reaction"):
                with mutating_discord(discord_message) as proxy:
                    await proxy.add_reaction(EMOJI_UNREAD)


async def create_message_data(client: ClubClient, member, content):
    return dict(
        content=content,
        embed=discord.Embed(
            color=discord.Color.from_rgb(120, 179, 84),
            description="Přečteno? Chceš další? Zaklikni zaškrtávátko pod touto zprávou a brzy ti pošlu další tip",
        ),
        allowed_mentions=discord.AllowedMentions(
            everyone=True,
            users=[
                await client.get_or_fetch_user(member_id)
                for member_id in [member.id] + ALLOWED_MENTIONS
            ],
            roles=False,
            replied_user=True,
        ),
    )


def prepare_messages(history, scheduled_messages, today, context=None):
    messages = []
    past_messages = {
        message.content_starting_emoji: message
        for message in history
        if message.content_starting_emoji in scheduled_messages
    }
    context = context or {}

    # append messages to edit
    for starting_emoji, message in past_messages.items():
        render_content = scheduled_messages[starting_emoji]
        scheduled_content = prepare_message_content(
            starting_emoji, render_content, context
        )
        if message.content != scheduled_content:
            messages.append((message.id, scheduled_content))

    # don't add a message twice the same day
    if past_messages:
        latest_past_message_on = sorted(
            past_messages.values(), key=attrgetter("created_at"), reverse=True
        )[0].created_at.date()
        if latest_past_message_on == today:
            return messages

    # don't add messages if the previous tip is unread
    if past_messages:
        last_message = sorted(
            past_messages.values(), key=attrgetter("created_at"), reverse=True
        )[0]
        if (
            last_message.reactions.get(EMOJI_UNREAD, 0) < 2
        ):  # bot prepares the emoji, then the user reacts, 1 + 1 = 2
            return messages

    # append messages to add
    for starting_emoji, render_content in scheduled_messages.items():
        if starting_emoji not in past_messages:
            scheduled_content = prepare_message_content(
                starting_emoji, render_content, context
            )
            messages.append((None, scheduled_content))
            break

    return messages


def prepare_message_content(emoji, render_content, context):
    return f"{emoji} {render_content(context).strip()}"
