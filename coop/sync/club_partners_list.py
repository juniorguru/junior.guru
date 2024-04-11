from datetime import timedelta
from pathlib import Path

import click
from discord import AllowedMentions, Color, Embed, File

from coop.cli.sync import main as cli
from coop.lib import discord_task, loggers
from coop.lib.discord_club import (
    ClubClient,
    is_message_over_period_ago,
    parse_channel,
)
from coop.lib.mutations import mutating_discord
from coop.models.base import db
from coop.models.club import ClubMessage
from coop.models.partner import Partnership


IMAGES_DIR = Path("coop/images")


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "partners"])
@click.option("--channel", "channel_id", default="partners_list", type=parse_channel)
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
    partnerships = list(Partnership.active_listing())
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
                "# Seznam partnerských firem\n\n"
                "Tyto firmy se podílejí na financování junior.guru. "
                "Můžeš se tady prokliknout na jejich stránky. "
                "Partnerství neznamená, že junior.guru doporučuje konkrétní kurzy, nebo že na ně nemáš psát recenze v klubu. "
                "\n\n"
                "Když sem partnerské firmy pošlou lidi, tak ti dostanou roli <@&837316268142493736> a k tomu ještě i roli pro konkrétní firmu, například <@&938306918097747968>. "
                "Role využívej a firmu označ, pokud po ní něco potřebuješ. "
                "Seznam firem je tady seřazený podle počtu lidí v klubu. "
            ),
            suppress=True,
            allowed_mentions=AllowedMentions.none(),
        )
    partners = sorted(
        [partnership.partner for partnership in partnerships],
        key=lambda partner: (len(partner.list_members), partner.name),
        reverse=True,
    )
    for partner in partners:
        logger.info(f"Posting {partner.name!r}")
        embed = Embed(
            title=partner.name,
            url=partner.url,
            color=Color.dark_grey(),
            description=f"Role: <@&{partner.role_id}>\nČlenů: {len(partner.list_members)}",
        )
        embed.set_thumbnail(url=f"attachment://{Path(partner.poster_path).name}")
        file = File(IMAGES_DIR / partner.poster_path)
        with mutating_discord(channel) as proxy:
            await proxy.send(
                embed=embed,
                file=file,
                allowed_mentions=AllowedMentions.none(),
            )
