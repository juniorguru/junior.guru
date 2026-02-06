from datetime import timedelta

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


CONTROL_EMOJI = "🧾"
REMINDER_PERIOD = timedelta(days=7)


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "candidates"])
def main():
    discord_task.run(sync_candidates_dms)


@db.connection_context()
async def sync_candidates_dms(client: ClubClient):
    candidates = []
    for candidate in Candidate.listing():
        if not candidate.is_member:
            continue
        if candidate.is_ready:
            continue
        if not candidate.user:
            logger.warning(f"Candidate {candidate.github_username} has no club user")
            continue
        if not candidate.user.dm_channel_id:
            logger.info(
                f"Candidate {candidate.github_username} has no DM channel, skipping"
            )
            continue
        if not candidate.report_url:
            logger.info(
                f"Candidate {candidate.github_username} has no report URL, skipping"
            )
            continue

        last_message = ClubMessage.last_bot_message(
            candidate.user.dm_channel_id, CONTROL_EMOJI
        )
        if not is_message_over_period_ago(last_message, REMINDER_PERIOD):
            logger.info(
                f"Candidate {candidate.github_username} already notified recently"
            )
            continue
        candidates.append(candidate)

    if not candidates:
        logger.info("No candidates to notify")
        return

    for candidate in candidates:
        logger.info(f"Notifying {candidate.github_username}")
        member = await client.club_guild.fetch_member(candidate.user.id)
        dm_channel = await get_or_create_dm_channel(member)
        if dm_channel is None:
            logger.warning(
                f"Could not open DM channel for {candidate.github_username}, skipping"
            )
            continue
        content = create_message(candidate)
        try:
            with mutating_discord(dm_channel) as proxy:
                await proxy.send(content)
        except Forbidden as exc:
            logger.error(f"Cannot send DM to {candidate.github_username}: {exc}")


def create_message(candidate: Candidate) -> str:
    name = candidate.name or candidate.github_username
    return (
        f"{CONTROL_EMOJI} Ahoj {name}, "
        "robot u tebe nasel veci, ktere je potreba doladit."
        f"\n\nReport: {candidate.report_url}"
        f"\nProfil: {candidate.profile_url}"
    )
