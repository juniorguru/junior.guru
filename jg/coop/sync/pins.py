import textwrap
from datetime import date, timedelta

import click
from discord import Embed, Forbidden

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, ClubEmoji, get_or_create_dm_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage, ClubPin


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--since", type=date.fromisoformat, default=f"{date.today() - timedelta(days=150)}"
)
def main(since: date):
    logger.info(f"Found {ClubPin.count()} pins in total")
    logger.info("Pairing existing pins saved in DMs with the messages they pin")
    with db.connection_context():
        for pinning_message in ClubMessage.pinning_listing():
            try:
                pinning_message.record_pin()
            except ClubPin.DoesNotExist:
                # This can happen if:
                #
                # - The message is older than what we have in the database. The bot has limited
                #   club memory, see DEFAULT_CHANNELS_HISTORY_SINCE and CHANNELS_HISTORY_SINCE.
                # - The message has been retro-actively deleted.
                # - The pin reaction has been retro-actively removed.
                message_url = pinning_message.pinned_message_url
                member_name = pinning_message.dm_member.display_name
                logger.debug(f"Could not find {message_url} pinned by {member_name!r}")
    discord_task.run(send_outstanding_pins, since)


@db.connection_context()
async def send_outstanding_pins(client: ClubClient, since):
    logger.info(f"Getting outstanding pins since {since}")
    for member_db, outstanding_pins in ClubPin.outstanding_by_member(since):
        logger.info(f"Sending outstanding pins to {member_db.display_name!r}")
        member = await client.club_guild.fetch_member(member_db.id)
        dm_channel = await get_or_create_dm_channel(member)
        for pin in outstanding_pins:
            content = f"{ClubEmoji.PIN} Vidím špendlík! Ukládám ti příspěvek sem, do soukromé zprávy."
            embed_description = [
                f"**{pin.pinned_message.author.display_name}** v kanálu „{pin.pinned_message.channel_name}”:",
                f"> {textwrap.shorten(pin.pinned_message.content, 500, placeholder='…')}",
                f"[Celý příspěvek]({pin.pinned_message.url})",
                "",
            ]
            logger.info(
                f"Pinning {pin.pinned_message.url} for {member_db.display_name!r} #{member_db.id}"
            )
            try:
                with mutating_discord(dm_channel) as proxy:
                    await proxy.send(
                        content=content,
                        embed=Embed(description="\n".join(embed_description)),
                    )
            except Forbidden:
                # TODO discord.errors.Forbidden: 403 Forbidden (error code: 50007): Cannot send messages to this user
                logger.exception(
                    f"Could not pin {pin.pinned_message.url} for {member_db.display_name!r} #{member_db.id}"
                )
