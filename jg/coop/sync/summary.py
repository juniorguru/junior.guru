from datetime import date, datetime, timedelta

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.llm import ask_for_json, count_tokens
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


SYSTEM_PROMPT = """
You are a Discord channel summarizer, providing clear and concise summaries
of the past messages in a specific Discord channel. User sends you a list
of messages, you reply with a JSON object of the following structure:

- summary (string)
    A brief summary of the channel's recent discussions. The summary should be to
    the point, concise. Max 20 sentences.
- topics (array[object])
    An array of the most notable topics discussed in the channel.

Each topic has the following structure:

- name (string)
    Name of the topic.
- message_id (int)
    The ID of the message that starts the topic.

The channel is about programming and entry-level careers, so that context
is implied and should not be mentioned.
"""


# Return a JSON object with key "topics", which will contain an array of 3 most
# notable topics discussed. Each topic should be a dictionary with the following keys:

# - title (string): Title of the topic, in Czech
# - message_id (int): The ID of the message that best represents or starts the topic

# The titles should use informal, conversational Czech, as can be found in texts
# by Honza Javorek (author of honzajavorek.cz and junior.guru). Keep them concise.
# Avoid too generic or sensational titles. No emojis, question or exclamation marks.

# Double check you're not inventing anything that isn't in the original messages.


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
    messages = list(ClubMessage.channel_listing(ClubChannelID.CHAT, since_at=since_at))
    logger.info(f"Found {len(messages)} messages")

    logger.info("Summarizing")
    user_prompt = "\n\n---\n\n".join(
        [
            f"Message #{n} by user <@{message.author.id}>:\n\n{message.content}"
            for n, message in enumerate(messages, start=1)
        ]
    )

    # FIXME
    return

    logger.debug(f"User prompt length: {count_tokens(user_prompt)} tokens")
    llm_response = await ask_for_json(SYSTEM_PROMPT, user_prompt)
    logger.debug(f"Summary: {llm_response['summary']}")
    for llm_topic in llm_response["topics"]:
        message_index = llm_topic["message_id"] - 1
        message = messages[message_index]
        logger.debug(f"Topic: {llm_topic['name']}, {message.url}")

    # TODO projet takhle vsechny kanaly, poresit i podvlakna
    # TODO udelat summary z jednotlivych summary


# def repr_message(message: ClubMessage) -> str:
#     meta = f"Message URL: {message.url}\nAuthor: <@{message.author.id}>\n"
#     if message.reactions:
#         reactions = ", ".join(
#             [f"{count}⨉{emoji}" for emoji, count in message.reactions.items()]
#         )
#         meta += f"Reactions: {reactions}\n"
#     return meta + f"\n{message.content}"
