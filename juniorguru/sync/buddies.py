from datetime import timedelta

import discord

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, HONZAJAVOREK,
                                 MENTORING_CHANNEL, is_message_bot_reminder,
                                 is_message_over_period_ago, run_discord_task)
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage


BUDDIES_CHANNEL = 822415540843839488

VOICE_CHANNEL = 769966887055392769

BUDDIES_EMOJI = '💡'


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content'])
def main():
    run_discord_task('juniorguru.sync.buddies.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(BUDDIES_CHANNEL, BUDDIES_EMOJI)
    if is_message_over_period_ago(last_message, timedelta(days=30)):
        logger.info('Last message is more than one month old!')
        if DISCORD_MUTATIONS_ENABLED:
            voice_channel = await client.fetch_channel(VOICE_CHANNEL)
            channel = await client.fetch_channel(BUDDIES_CHANNEL)
            await channel.purge(check=is_message_bot_reminder)
            await channel.send(content=(
                f"{BUDDIES_EMOJI} Nezapomeň, že si tady můžeš hledat parťáky na společné učení "
                f"nebo projekt. Pokud utvoříte skupinu, napište <@{HONZAJAVOREK}> "
                "a vytvoří vám tady v klubu roli a soukromý kanál, kde se můžete domlouvat. "
                f"Hlasový kanál {voice_channel.mention} může kdokoliv z klubu využívat k volání jak potřebuje, "
                "takže si tam klidně můžete dávat schůzky."
                "\n\n"
                "💁 Pomohlo by ti pravidelně si s někým na hodinku zavolat a probrat svůj postup? "
                f"Mrkni do <#{MENTORING_CHANNEL}>, kde je seznam členů, kteří se k takovým "
                "konzultacím nabídli."
            ), allowed_mentions=discord.AllowedMentions.none())
        else:
            logger.warning('Discord mutations not enabled')
