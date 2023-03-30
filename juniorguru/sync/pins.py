import asyncio
import textwrap

from discord import Embed
from discord.errors import Forbidden

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
# from juniorguru.lib import mutations
# from juniorguru.lib.discord_club import ClubMemberID
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubPinReaction


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content'])
def main():
    discord_sync.run(ensure_pins_are_in_dms)


@db.connection_context()
async def ensure_pins_are_in_dms(client):
    # TODO
    # member = await client.club_guild.fetch_member(ClubMemberID.HONZA)
    # with mutations.allowing_discord():
    #     dm_channel = await member.create_dm()
    # message = await dm_channel.fetch_message(1089766546441785354)
    # from pprint import pprint
    # print(repr(message.embeds[0].description))
    # return
    pin_reactions = ClubPinReaction.listing()
    logger.info(f'Found {len(pin_reactions)} pin reactions by people who are currently members')
    await asyncio.gather(*[
        process_pin_reaction(client, pin_reaction)
        for pin_reaction in pin_reactions
    ])


async def process_pin_reaction(client, pin_reaction):
    logger_p = logger[f'reactions.{pin_reaction.id}']

    member = await client.club_guild.fetch_member(pin_reaction.member.id)
    if member.dm_channel:
        channel = member.dm_channel
    else:
        logger_p.debug(f"Creating DM channel for {member.display_name} #{member.id}")
        channel = await member.create_dm()

    logger_p.debug(f"Checking DM if already pinned for {member.display_name} #{member.id}")
    if await is_pinned(pin_reaction.message.url, channel):
        logger_p.debug(f"Already pinned for {member.display_name} #{member.id}")
        return

    logger_p.debug(f"Not pinned for {member.display_name} #{member.id}, sending a message to DM")
    content = (
        '📌 Vidím špendlík! Ukládám ti příspěvek sem, do soukromé zprávy.'
    )
    embed_description = [
        f"**{pin_reaction.message.author.display_name}** v kanálu „{pin_reaction.message.channel_name}”:",
        f"> {textwrap.shorten(pin_reaction.message.content, 500, placeholder='…')}",
        f"[Celý příspěvek]({pin_reaction.message.url})",
        "",
    ]
    try:
        with mutating_discord(channel) as proxy:
            await proxy.send(content=content, embed=Embed(description="\n".join(embed_description)))
    except Forbidden as e:
        logger_p.error(str(e), exc_info=True)


async def is_pinned(message_url, channel):
    async for message in channel.history(limit=None, after=None):
        starts_with_pin_emoji = message.content.startswith('📌')
        contains_message_url = any([message_url in embed.description for embed in message.embeds])
        if starts_with_pin_emoji and contains_message_url:
            return True
    return False
