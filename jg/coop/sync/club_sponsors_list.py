from datetime import timedelta
from pathlib import Path

import click
from discord import AllowedMentions, Color, Embed, File

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubClient,
    is_message_over_period_ago,
    parse_channel,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.sponsor import Sponsor


IMAGES_DIR = Path("jg/coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "organizations", "roles"])
@click.option("--channel", "channel_id", default="sponsors_list", type=parse_channel)
@click.option(
    "--recreate-interval",
    "recreate_interval_days",
    default=30,
    type=int,
    help="In days.",
)
def main(channel_id: int, recreate_interval_days: int):
    discord_task.run(recreate_archive, channel_id, recreate_interval_days)


@db.connection_context()
async def recreate_archive(
    client: ClubClient, channel_id: int, recreate_interval_days: int
):
    sponsors = Sponsor.club_listing()
    messages = ClubMessage.channel_listing(channel_id, by_bot=True)
    try:
        last_message = messages[-1]
    except IndexError:
        logger.info("No messages in the channel")
    else:
        if is_message_over_period_ago(
            last_message, timedelta(days=recreate_interval_days)
        ):
            logger.info("Channel content is too old")
        else:
            logger.info("Channel content is recent, skipping")
            return

    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.purge(limit=None)
    with mutating_discord(channel) as proxy:
        await proxy.send(
            (
                "# Seznam sponzorů\n\n"
                "Tyto organizace se podílejí na financování junior.guru. "
                "Můžeš se tady prokliknout na jejich stránky. "
                "Sponzorství neznamená, že junior.guru doporučuje konkrétní kurzy, nebo že na ně nemáš psát recenze v klubu. "
                "\n\n"
                "Když sem sponzoři pošlou lidi, tak ti dostanou roli <@&837316268142493736> a k tomu ještě i roli pro konkrétní subjekt, například <@&938306918097747968>. "
                "Role využívej a sponzory klidně označ, pokud po nich něco potřebuješ. "
                "Seznam sponzorů je tady seřazený podle počtu jejich lidí v klubu. "
            ),
            suppress=True,
            allowed_mentions=AllowedMentions.none(),
        )
    for sponsor in sponsors:
        logger.info(f"Posting {sponsor.name!r}")
        embed = Embed(
            title=sponsor.name,
            url=sponsor.url,
            color=Color.dark_grey(),
            description=f"Role: <@&{sponsor.role_id}>\nČlenů: {sponsor.members_count}",
        )
        embed.set_thumbnail(url=f"attachment://{Path(sponsor.poster_path).name}")
        file = File(IMAGES_DIR / sponsor.poster_path)
        with mutating_discord(channel) as proxy:
            await proxy.send(
                embed=embed,
                file=file,
                allowed_mentions=AllowedMentions.none(),
            )
