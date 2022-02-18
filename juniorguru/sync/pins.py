import asyncio
import textwrap

from discord import Embed
from discord.errors import Forbidden

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, is_discord_mutable
from juniorguru.models import ClubPinReaction, ClubUser, ClubMessage, db


logger = loggers.get(__name__)


@measure()
def main():
    run_discord_task('juniorguru.sync.pins.discord_task')


@db.connection_context()
async def discord_task(client):
    top_members_limit = ClubUser.top_members_limit()
    pin_reactions = [pin_reaction for pin_reaction
                     in ClubPinReaction.listing()
                     if pin_reaction.user.is_member]

    logger.info(f'Found {len(pin_reactions)} pin reactions by people who are currently members')
    await asyncio.gather(*[
        process_pin_reaction(client, pin_reaction, top_members_limit)
        for pin_reaction in pin_reactions
    ])

    logger.info(f"Going through messages pinned by reactions, minimum is {top_members_limit} pin reactions")
    messages = ClubMessage.pinned_by_reactions_listing(top_members_limit)

    logger.info(f'Found {len(messages)} messages')
    await asyncio.gather(*[
        process_message(client, message, top_members_limit)
        for message in messages
    ])


async def process_pin_reaction(client, pin_reaction, top_members_limit):
    pin_logger = logger.getChild(f'reactions.{pin_reaction.id}')

    member = await client.juniorguru_guild.fetch_member(pin_reaction.user.id)
    if member.dm_channel:
        channel = member.dm_channel
    else:
        pin_logger.debug(f"Creating DM channel for {member.display_name} #{member.id}")
        channel = await member.create_dm()

    pin_logger.debug(f"Checking DM if already pinned for {member.display_name} #{member.id}")
    if await is_pinned(pin_reaction.message.url, channel):
        pin_logger.debug(f"Already pinned for {member.display_name} #{member.id}")
        return

    pin_logger.debug(f"Not pinned for {member.display_name} #{member.id}, sending a message to DM")
    if is_discord_mutable():
        content = (
            '📌 Vidím špendlík! Ukládám ti příspěvek sem, do soukromé zprávy. '
            f'Když bude mít zhruba {top_members_limit} špendlíků, připnu jej '
            'v původním kanálu pro všechny.'
        )
        embed_description = [
            f"{pin_reaction.message.author.mention} v {pin_reaction.message.channel_mention}:",
            f"> {textwrap.shorten(pin_reaction.message.content, 500, placeholder='…')}",
            f"[Hop na příspěvek]({pin_reaction.message.url})",
            "",
        ]
        try:
            await channel.send(content=content,
                               embed=Embed(description="\n".join(embed_description)))
        except Forbidden as e:
            pin_logger.error(str(e), exc_info=True)


async def is_pinned(message_url, channel):
    async for message in channel.history(limit=None, after=None):
        starts_with_pin_emoji = message.content.startswith('📌')
        contains_message_url = any([message_url in embed.description for embed in message.embeds])
        if starts_with_pin_emoji and contains_message_url:
            return True
    return False


async def process_message(client, message, top_members_limit):
    message_logger = loggers.get(f'pins.messages.{message.id}')
    message_logger.debug(f"Message {message.url} {'PINNED' if message.is_pinned else 'NOT PINNED'}")
    if not message.is_pinned:
        message_logger.info(f"Pinning {message.url}")
        if is_discord_mutable():
            channel = await client.fetch_channel(message.channel_id)
            discord_message = await channel.fetch_message(message.id)
            await discord_message.pin(reason=f"The message has {message.pin_reactions_count} pin reactions, minimum is {top_members_limit}")


if __name__ == '__main__':
    main()
