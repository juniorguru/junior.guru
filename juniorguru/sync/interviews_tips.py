from datetime import timedelta

from discord import Color, Embed

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (DISCORD_MUTATIONS_ENABLED, ClubChannel,
                                         is_message_over_period_ago)
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.mentor import Mentor


INTERVIEWS_EMOJI = '💁'


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content', 'mentoring'])
def main():
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(ClubChannel.INTERVIEWS, INTERVIEWS_EMOJI)
    if is_message_over_period_ago(last_message, timedelta(days=30)):
        logger.info('Last message is more than one month old!')
        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(ClubChannel.INTERVIEWS)

            embed_mentors_description = '\n'.join([
                f'[{mentor.user.display_name}]({mentor.message_url}) – {mentor.topics}'
                for mentor in Mentor.interviews_listing()
            ])
            embed_mentors = Embed(color=Color.orange(),
                                  description=embed_mentors_description)

            embed_handbook = Embed(description=(
                '📖 Než se pustíš do pohovorů, přečti si '
                '[příručku na junior.guru](https://junior.guru/handbook/candidate/) o tom, '
                'jak správně hledat první práci v IT.'
            ))

            await channel.send(content=(
                f"{INTERVIEWS_EMOJI} Pomohla by ti soustavnější příprava na přijímací řízení? "
                "Chceš si jednorázově vyzkoušet pohovor nanečisto, česky nebo anglicky? "
                f"Někteří členové se v <#{ClubChannel.MENTORING}> k takovým konzultacím nabídli!"
            ), embeds=[embed_mentors, embed_handbook])
        else:
            logger.warning('Discord mutations not enabled')
