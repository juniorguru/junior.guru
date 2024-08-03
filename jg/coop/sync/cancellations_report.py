import re
from datetime import date

import click
from discord import Embed, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.memberful import memberful_url
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.subscription import (
    SubscriptionCancellation,
    SubscriptionCancellationReason,
)


logger = loggers.from_path(__file__)


REPORT_EMOJI = "💔"

ID_RE = re.compile(r"`#(\d+)`")


@cli.sync_command(dependencies=["club-content", "subscriptions-csv"])
@click.option("--channel", "channel_id", default="business", type=parse_channel)
def main(channel_id: int):
    discord_task.run(report, channel_id)


@db.connection_context()
async def report(client: ClubClient, channel_id: int):
    today = date.today()
    account_ids = [
        int(ID_RE.search(message.content).group(1))
        for message in ClubMessage.channel_listing(
            channel_id, starting_emoji=REPORT_EMOJI, by_bot=True
        )
    ]
    logger.debug(f"Found {len(account_ids)} reported cancellations")

    cancellations = SubscriptionCancellation.report_listing(
        exclude_account_ids=account_ids
    )
    logger.debug(f"About to report {len(cancellations)} cancellations")

    for cancellation in cancellations:
        logger.debug(f"Reporting cancellation: {cancellation.account_name}")
        # initial message content
        if cancellation.reason == SubscriptionCancellationReason.AFFORDABILITY:
            message_content = f"{REPORT_EMOJI}💰 "
        else:
            message_content = f"{REPORT_EMOJI} "

        # initial embed and buttons
        embed_description = (
            f"**Kdo:** {cancellation.account_name}, {cancellation.account_email}\n"
            f"**Utraceno:** {cancellation.account_total_spend} Kč\n"
        )
        buttons = [
            ui.Button(
                emoji="💳",
                label="Memberful",
                url=memberful_url(cancellation.account_id),
            )
        ]

        # data depending on whether the user is on Discord
        if user := cancellation.user:
            message_content += f"{user.mention}"
            embed_description += f"**Písmenek v klubu**: {user.content_size()}\n"
            if cancellation.expires_on:
                months = int(
                    (cancellation.expires_on - user.joined_at.date()).days / 30
                )
                embed_description += f"**Měsíců v klubu**: {months}\n"
            if intro_message := user.intro:
                buttons.append(
                    ui.Button(emoji="👋", label="#ahoj", url=intro_message.url)
                )
        else:
            message_content += f"**{cancellation.account_name}**"

        # id
        message_content += f" ruší členství! `#{cancellation.account_id}`"

        # remaining days
        if cancellation.expires_on and cancellation.expires_on > today:
            embed_description += (
                f"**Zbývá dní:** {(cancellation.expires_on - today).days}\n"
            )

        # reason and feedback
        embed_description += f"**Důvod:** `{cancellation.reason.upper()}`\n"
        if cancellation.feedback:
            embed_description += f"> {cancellation.feedback}\n"

        # send it!
        channel = await client.fetch_channel(channel_id)
        with mutating_discord(channel) as proxy:
            embed = Embed(description=embed_description)
            await proxy.send(
                content=message_content, embed=embed, view=ui.View(*buttons)
            )
