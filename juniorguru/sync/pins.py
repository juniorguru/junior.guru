import asyncio
import textwrap

from discord import Embed
from discord.errors import Forbidden

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubPinReaction
from juniorguru.sync.club_content import main as club_content_task


logger = loggers.get(__name__)


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.pins.discord_task')


@db.connection_context()
async def discord_task(client):
    pin_reactions = ClubPinReaction.members_listing()
    logger.info(f'Found {len(pin_reactions)} pin reactions by people who are currently members')
    await asyncio.gather(*[
        process_pin_reaction(client, pin_reaction)
        for pin_reaction in pin_reactions
    ])


async def process_pin_reaction(client, pin_reaction):
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
    if DISCORD_MUTATIONS_ENABLED:
        content = (
            '📌 Vidím špendlík! Ukládám ti příspěvek sem, do soukromé zprávy.'
        )
        embed_description = [
            f"**{pin_reaction.message.author.display_name}** v {pin_reaction.message.channel_mention}:",
            f"> {textwrap.shorten(pin_reaction.message.content, 500, placeholder='…')}",
            f"[Hop na příspěvek]({pin_reaction.message.url})",
            "",
        ]
        try:
            await channel.send(content=content,
                               embed=Embed(description="\n".join(embed_description)))
        except Forbidden as e:
            pin_logger.error(str(e), exc_info=True)
    else:
        logger.warning('Discord mutations not enabled')


async def is_pinned(message_url, channel):
    async for message in channel.history(limit=None, after=None):
        starts_with_pin_emoji = message.content.startswith('📌')
        contains_message_url = any([message_url in embed.description for embed in message.embeds])
        if starts_with_pin_emoji and contains_message_url:
            return True
    return False
