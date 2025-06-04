import json
from datetime import date, datetime, timedelta
from pprint import pp

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.llm import ask_for_json
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


SYSTEM_PROMPT = """
You get a history of messages from a specific Discord channel, and your
task is to summarize the key topics and highlights. Consider also reactions,
as they indicate what the community found important or interesting.

Return a JSON object with key "topics", which will contain an array of topics
discussed. Each topic should be a dictionary with the following keys:

- title (string): Title of the topic, in Czech
- message_id (int): The ID of the message that best represents or starts the topic

The titles should use informal, conversational Czech, as if you were explaining
the topics to a friend. Keep them concise, around 5-10 words. Avoid too generic
titles. The whole Discord is about programming and entry level careers, so framing
of the topics in that context is already implied.

Double check you're not inventing anything that isn't in the original messages.
"""


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--days", default=30, type=int)
@db.connection_context()
@async_command
async def main(today: date, days: int):
    since_at = datetime.combine(today - timedelta(days=days), datetime.min.time())
    logger.info(f"Summarizing since: {since_at.date()}")
    return
    messages = ClubMessage.channel_listing(ClubChannelID.CHAT, since_at=since_at)
    feed = [
        {
            "id": message.id,
            "author_id": message.author.id,
            "markdown": message.content,
            "reactions": message.reactions,
        }
        for message in messages
    ]
    llm_reply = await ask_for_json(json.dumps(feed, ensure_ascii=False), SYSTEM_PROMPT)
    topics = [
        f"{item['title']}: https://discord.com/channels/769966886598737931/{ClubChannelID.CHAT}/{item['message_id']}"
        for item in llm_reply["topics"]
    ]
    pp(topics)
