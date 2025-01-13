import re

import click
from discord import Embed, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.memberful import memberful_url
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.subscription import SubscriptionMarketingSurvey


logger = loggers.from_path(__file__)


REPORT_EMOJI = "👋"

ID_RE = re.compile(r"`#(\d+)`")


@cli.sync_command(dependencies=["club-content", "subscriptions-csv"])
@click.option("--channel", "channel_id", default="business", type=parse_channel)
def main(channel_id):
    discord_task.run(report, channel_id)


@db.connection_context()
async def report(client: ClubClient, channel_id: int):
    account_ids = [
        int(ID_RE.search(message.content).group(1))
        for message in ClubMessage.channel_listing(
            channel_id, starting_emoji=REPORT_EMOJI, by_bot=True
        )
    ]
    logger.debug(f"Found {len(account_ids)} reported marketing survey answers")

    answers = SubscriptionMarketingSurvey.report_listing(
        exclude_account_ids=account_ids
    )
    logger.debug(f"About to report {len(answers)} marketing survey answers")

    for answer in answers:
        logger.debug(f"Reporting marketing survey answer: {answer.account_name}")
        # initial data
        message_content = f"{REPORT_EMOJI} "
        embed_description = f"**Odkud:** `{answer.type.upper()}`\n> {answer.value}\n"
        buttons = [
            ui.Button(
                emoji="💳", label="Memberful", url=memberful_url(answer.account_id)
            )
        ]

        # data depending on whether the user is on Discord
        if user := answer.user:
            message_content += f"{user.mention}"
            if intro_message := user.intro:
                buttons.append(
                    ui.Button(emoji="👋", label="#ahoj", url=intro_message.url)
                )
        else:
            message_content += f"**{answer.account_name}**"

        # id
        message_content += f" je v klubu! `#{answer.account_id}`"

        # send it!
        channel = await client.fetch_channel(channel_id)
        with mutating_discord(channel) as proxy:
            embed = Embed(description=embed_description)
            await proxy.send(
                content=message_content, embed=embed, view=ui.View(*buttons)
            )
