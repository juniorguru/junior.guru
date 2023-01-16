import asyncio
from datetime import date
from operator import attrgetter

import discord

from juniorguru.lib import loggers
from juniorguru.lib.asyncio_extra import chunks
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, emoji_name
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.sync.onboarding.scheduled_messages import (ALLOWED_MENTIONS,
                                                           SCHEDULED_MESSAGES)


TODAY = date.today()

MEMBERS_CHUNK_SIZE = 10

EMOJI_UNREAD = '✅'


logger = loggers.from_path(__file__)


async def send_messages(client):
    members_chunks = chunks(ClubUser.onboarding_listing(),
                            size=MEMBERS_CHUNK_SIZE)
    for n, members_chunk in enumerate(members_chunks, start=1):
        logger.debug(f'Processing chunk #{n} of {len(members_chunk)} members')
        await asyncio.gather(*[
            send_messages_to_member(client, member)
            for member in members_chunk
        ])


async def send_messages_to_member(client, member):
    logger_m = logger[f'members.{member.id}']
    logger_m.debug('Preparing messages')
    messages = prepare_messages(ClubMessage.channel_listing_bot(member.onboarding_channel_id),
                                SCHEDULED_MESSAGES, TODAY, context=dict(member=member))
    if not messages:
        logger_m.debug('Nothing to do')
        return
    logger_m.info(f'Processing {len(messages)} messages')

    channel = await client.fetch_channel(member.onboarding_channel_id)
    for message_id, message_content in messages:
        if message_id:
            logger_m.debug(f'Editing message {message_content[0]}: {len(message_content)} characters')
            if DISCORD_MUTATIONS_ENABLED:
                discord_message = await channel.fetch_message(message_id)
                message_data = await create_message_data(client, member, message_content)
                await discord_message.edit(**message_data)
                if not get_reaction(discord_message.reactions, EMOJI_UNREAD):
                    await discord_message.add_reaction(EMOJI_UNREAD)
            else:
                logger_m.warning('Discord mutations not enabled')
        else:
            logger_m.debug(f'Sending message {message_content[0]}: {len(message_content)} characters')
            if DISCORD_MUTATIONS_ENABLED:
                message_data = await create_message_data(client, member, message_content)
                discord_message = await channel.send(**message_data)
                await discord_message.add_reaction(EMOJI_UNREAD)
            else:
                logger_m.warning('Discord mutations not enabled')


def get_reaction(reactions, emoji):
    for reaction in reactions:
        if emoji_name(reaction.emoji) == emoji:
            return reaction
    return None


async def create_message_data(client, member, content):
    return dict(content=content,
                embed=discord.Embed(color=discord.Color.from_rgb(120, 179, 84),
                                    description='Přečteno? Chceš další? Zaklikni zaškrtávátko pod touto zprávou a brzy ti pošlu další tip'),
                allowed_mentions=discord.AllowedMentions(everyone=True,
                                                         users=[await client.get_or_fetch_user(member_id)
                                                                for member_id in [member.id] + ALLOWED_MENTIONS],
                                                         roles=False,
                                                         replied_user=True))


def prepare_messages(history, scheduled_messages, today, context=None):
    messages = []
    past_messages = {message.emoji_prefix: message
                     for message in history
                     if message.emoji_prefix in scheduled_messages}
    context = context or {}

    # append messages to edit
    for emoji_prefix, message in past_messages.items():
        render_content = scheduled_messages[emoji_prefix]
        scheduled_content = prepare_message_content(emoji_prefix, render_content, context)
        if message.content != scheduled_content:
            messages.append((message.id, scheduled_content))

    # don't add a message twice the same day
    if past_messages:
        latest_past_message_on = sorted(past_messages.values(),
                                        key=attrgetter('created_at'),
                                        reverse=True)[0].created_at.date()
        if latest_past_message_on == today:
            return messages

    # don't add messages if the previous tip is unread
    if past_messages:
        last_message = sorted(past_messages.values(),
                              key=attrgetter('created_at'),
                              reverse=True)[0]
        if last_message.reactions.get(EMOJI_UNREAD, 0) < 2:  # bot prepares the emoji, then the user reacts, 1 + 1 = 2
            return messages

    # append messages to add
    for emoji_prefix, render_content in scheduled_messages.items():
        if emoji_prefix not in past_messages:
            scheduled_content = prepare_message_content(emoji_prefix, render_content, context)
            messages.append((None, scheduled_content))
            break

    return messages


def prepare_message_content(emoji, render_content, context):
    return f'{emoji} {render_content(context).strip()}'
