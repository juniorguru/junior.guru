import json
from datetime import date, datetime, timedelta

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.chunks import chunks
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.llm import ask_for_json
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


SYSTEM_PROMPT = """
You are a Discord channel summarizer, providing clear and concise summaries
of the past messages in a specific Discord channel. The channel is about
programming and entry-level careers, so your summaries should imply that context.

Return a JSON object with key "topics", which will contain an array of 3 most
notable topics discussed. Each topic should be a dictionary with the following keys:

- title (string): Title of the topic, in Czech
- message_id (int): The ID of the message that best represents or starts the topic

The titles should use informal, conversational Czech, as can be found in texts
by Honza Javorek (author of honzajavorek.cz and junior.guru). Keep them concise.
Avoid too generic or sensational titles. No emojis, question or exclamation marks.

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
    messages = list(ClubMessage.channel_listing(ClubChannelID.CHAT, since_at=since_at))
    prev_topics = []
    for messages_chunk in chunks(messages, size=len(messages) // 4):
        feed = [
            {
                "id": message.id,
                "author_id": message.author.id,
                "markdown": message.content,
                "reactions": message.reactions,
            }
            for message in messages_chunk
        ]
        prompt = json.dumps(feed, ensure_ascii=False)
        if prev_topics:
            prompt = (
                f"Right before the message history below, these topics were previously discussed: {', '.join(prev_topics)}"
                f"\n\n{prompt}"
            )
        llm_reply = await ask_for_json(prompt, SYSTEM_PROMPT)
        for item in llm_reply["topics"]:
            print(
                f"{item['title']}: https://discord.com/channels/769966886598737931/{ClubChannelID.CHAT}/{item['message_id']}"
            )
        prev_topics = [item["title"] for item in llm_reply["topics"]]
