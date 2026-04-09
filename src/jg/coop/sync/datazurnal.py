import click
import feedparser
import httpx
from discord.abc import GuildChannel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.reading_time import reading_time
from jg.coop.lib.text import extract_text
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


logger = loggers.from_path(__file__)

EMOJI = "📰"


@cli.sync_command(dependencies=["club-content"])
@click.option("--channel", "channel_id", default="1421171257164038231", type=parse_channel)
@click.option("--rss-url", default="https://samizdat.cz/rss.xml")
@db.connection_context()
def main(channel_id: int, rss_url: str):
    logger.info(f"Reading RSS: {rss_url}")
    response = httpx.get(rss_url)
    response.raise_for_status()
    if not (articles := feedparser.parse(response.content).entries):
        logger.warning("No articles found in RSS feed")
        return

    latest = articles[0]
    logger.info(f"Latest article: {latest.title!r} {latest.link}")

    if message := ClubMessage.last_bot_message(
        channel_id, starting_emoji=EMOJI, contains_text=latest.link
    ):
        logger.info(f"Already posted: {message.url}")
        return

    if not (content := latest.get("content")):
        raise RuntimeError(f"Article has no content: {latest.link}")
    content_html = content[0].value
    mins = reading_time(len(extract_text(content_html)))

    logger.info("Posting new article")
    discord_task.run(post, channel_id, latest.title, latest.link, mins)


@mutations.mutates_discord()
async def post(
    client: ClubClient, channel_id: int, title: str, url: str, mins: int
) -> None:
    channel: GuildChannel = client.get_channel(channel_id)
    logger.info(f"Posting to channel {channel.name!r}")
    await channel.send(
        f"{EMOJI} Hele, vyšel nový Datažurnál! ({mins} min čtení)\n\n**{title}**\n{url}"
    )
