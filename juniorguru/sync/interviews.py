from datetime import timedelta

import click
from discord import Color, Embed

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, MENTORING_CHANNEL,
                                 is_message_over_period_ago, run_discord_task)
from juniorguru.cli.sync import Command
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.mentor import Mentor


INTERVIEWS_CHANNEL = 789107031939481641

INTERVIEWS_EMOJI = '💁'


logger = loggers.get(__name__)


@click.command(cls=Command, requires=['club-content',
                        'mentoring'])
def main():
    run_discord_task('juniorguru.sync.interviews.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(INTERVIEWS_CHANNEL, INTERVIEWS_EMOJI)
    if is_message_over_period_ago(last_message, timedelta(days=30)):
        logger.info('Last message is more than one month old!')
        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(INTERVIEWS_CHANNEL)

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
                f"Někteří členové se v <#{MENTORING_CHANNEL}> k takovým konzultacím nabídli!"
            ), embeds=[embed_mentors, embed_handbook])
        else:
            logger.warning('Discord mutations not enabled')
