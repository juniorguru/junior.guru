import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.job import DroppedJob, ListedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-listing"])
@click.option("--channel", "channel_id", default="jobs_trash", type=parse_channel)
@click.option("--sample-size", default=10, type=int)
@db.connection_context()
def main(channel_id: int, sample_size: int):
    discord_task.run(sync_trash, channel_id, sample_size)


async def sync_trash(client: ClubClient, channel_id: int, sample_size: int):
    channel = await client.club_guild.fetch_channel(channel_id)

    logger.info(f"Emptying #{channel.name}")
    with mutating_discord(channel) as proxy:
        await proxy.purge()

    dropped_count = DroppedJob.count()
    listed_count = ListedJob.count()
    logger.info(f"Stats: listed={listed_count}, dropped={dropped_count}")
    with mutating_discord(channel) as proxy:
        await proxy.send(f"ℹ️ Juniorní: {listed_count}, ostatní: {dropped_count}")

    for job in DroppedJob.sample_listing(sample_size):
        logger.info(f"Posting: {job.url}")
        with mutating_discord(channel) as proxy:
            await proxy.send(
                f"**{job.title}**\n> {job.reason}\n{job.url}", suppress=True
            )
