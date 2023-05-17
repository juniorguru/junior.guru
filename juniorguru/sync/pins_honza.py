import textwrap

from discord import Embed

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import ClubEmoji, get_or_create_dm_channel
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubPin


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['pins'])
def main():
    pass

    # Read Honza's pins from database
    # Check if there are reactions
    # If not, add all the buttons
    # If yes, check buttons
    # If some buttons pressed, and ✅ is pressed, skip
    # If some buttons pressed, and ✅ not pressed, add the pin to respective pages and press ✅

    # logger.info(f'Found {ClubPin.count()} pins in total')
    # logger.info('Pairing existing pins saved in DMs with the messages they pin')
    # with db.connection_context():
    #     for pinning_message in ClubMessage.pinning_listing():
    #         try:
    #             pinning_message.record_pin()
    #         except ClubPin.DoesNotExist:
    #             # This can happen if:
    #             #
    #             # - The message is older than what we have in the database. The bot has limited
    #             #   club memory, see DEFAULT_CHANNELS_HISTORY_SINCE and CHANNELS_HISTORY_SINCE.
    #             # - The message has been retro-actively deleted.
    #             # - The pin reaction has been retro-actively removed.
    #             message_url = pinning_message.pinned_message_url
    #             member_name = pinning_message.dm_member.display_name
    #             logger.debug(f"Could not find {message_url} pinned by {member_name!r}")
    # discord_sync.run(send_outstanding_pins)
