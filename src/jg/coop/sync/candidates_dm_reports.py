from datetime import timedelta

import click
from discord.errors import Forbidden

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubClient,
    get_or_create_dm_channel,
    is_message_over_period_ago,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate
from jg.coop.models.club import ClubMessage


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "candidates"])
@click.option("--cooldown-days", default=7, type=int)
@click.option("--emoji", default="🦸")
def main(cooldown_days: int, emoji: str):
    discord_task.run(sync_candidates_dms, cooldown_days, emoji)


@db.connection_context()
async def sync_candidates_dms(client: ClubClient, cooldown_days: int, emoji: str):
    candidates = []
    for candidate in Candidate.dm_reports_listing():
        last_message = ClubMessage.last_bot_message(candidate.user.dm_channel_id, emoji)
        if is_message_over_period_ago(last_message, timedelta(days=cooldown_days)):
            candidates.append(candidate)
        else:
            logger.info(
                f"Candidate {candidate.github_username} already notified recently"
            )
    if not candidates:
        logger.info("No candidates to notify")
        return
    for candidate in candidates:
        logger.info(
            f"Notifying @{candidate.github_username} about {candidate.report_url}"
        )
        member = await client.club_guild.fetch_member(candidate.user.id)
        if dm_channel := await get_or_create_dm_channel(member):
            try:
                with mutating_discord(dm_channel) as proxy:
                    await proxy.send(**create_message(candidate, emoji))
            except Forbidden:
                logger.warning(
                    f"Could not send DM to {candidate.github_username}, skipping"
                )
        else:
            logger.warning(
                f"Could not open DM for {candidate.github_username}, skipping"
            )


def create_message(candidate: Candidate, emoji: str) -> str:
    return dict(
        content=(
            f"{emoji} Ahoj! "
            "Tvůj profil na [junior.guru/candidates](https://junior.guru/candidates) "
            f"[má nedostatky]({candidate.report_url}), takže je v seznamu kandidátů upozaděný.\n\n"
            "Lidi občas nesledují notifikace z GitHubu, takže ti to raději posílám i takhle. "
            "Stačí, když si opravíš 🔴 červené věci a zobrazíš se opět naplno. "
            "Pokud už profil nepotřebuješ, pošli Pull Request, kde svůj YAML soubor mažeš."
        )
    )
