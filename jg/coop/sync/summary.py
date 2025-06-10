import asyncio
from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter
from typing import Iterable

import click
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.llm import ask_for_json
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


SYSTEM_PROMPT_TEMPLATE = """
You are a Discord {container} summarizer. You summarize recent activity across a {container} focused on learning programming and early-career topics. You get a list of {items}. You respond with a JSON object with two fields:

- text (string): Write exactly what was discussed. No intros, no conclusions, no commentary about the server or atmosphere. Only facts about topics, opinions, and resources shared. Write plain, short sentences. Maximum 3 paragraphs, each up to 5 sentences.
- topics (array of objects): Key discussion topics pulled from the summaries. Each topic has:
    - name (string): What the topic was about.
    - message_id (int): The ID of the message that started that topic.

Tone: Professional but casual. No filler words or flowery language. Avoid vague words like "reflected," "resonated," "commitment," or "exchange." Just state the facts plainly.

Example:
```
{{
  "text": "Members discussed AI's impact on programming jobs and the reliability of Stack Overflow. They debated how job requirements are changing with new tech.\n\nSeveral shared their experiences switching careers to programming, highlighting bootcamps, job applications, and key skills.\n\nThere were recommendations for online courses, AI testing tools, and frameworks for beginners. Members talked about personal projects and networking.",
  "topics": [
    {{
      "name": "AI and programming jobs",
      "message_id": 1234567890
    }},
    {{
      "name": "The fate of Stack Overflow",
      "message_id": 1234567891
    }}
  ]
}}
```
"""


class Topic(BaseModel):
    name: str
    message_id: int


class Summary(BaseModel):
    text: str
    topics: list[Topic]


class ChannelStats(BaseModel):
    messages_count: int
    authors_count: int
    reactions_count: int
    content_size: int


class ChannelSummary(BaseModel):
    stats: ChannelStats
    summary: Summary


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
    since_on = today - timedelta(days=days)
    logger.info(f"Summarizing since: {since_on}")
    messages = ClubMessage.summary_listing(since_on=since_on)
    tasks = [
        asyncio.create_task(summarize_channel(list(channel_messages)))
        for _, channel_messages in groupby(messages, key=attrgetter("channel_id"))
    ]
    logger.info(f"Waiting for {len(tasks)} summaries")
    summaries = [s for s in await asyncio.gather(*tasks) if s is not None]

    logger.info(f"Waiting for a summary of {len(summaries)} channels")
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(container="server", items="channels")
    llm_response = await ask_for_json(
        system_prompt, serialize_channel_summaries(summaries)
    )
    summary = Summary(**llm_response)
    logger.info(f"Summary text:\n\n{summary.text}")
    for topic in summary.topics:
        message = ClubMessage.get_by_id(topic.message_id)
        logger.info(f"Topic: {topic.name}, {message.url}")

    # TODO
    # informal, conversational Czech, as can be found in texts
    # by Honza Javorek (author of honzajavorek.cz and junior.guru). Keep them concise.
    # Avoid too generic or sensational titles. No emojis, question or exclamation marks.


async def summarize_channel(messages: list[ClubMessage]) -> ChannelSummary | None:
    name = messages[0].channel_name
    stats = ChannelStats(
        messages_count=len(messages),
        authors_count=len(set(m.author.id for m in messages)),
        reactions_count=sum(sum(m.reactions.values()) for m in messages),
        content_size=sum(m.content_size for m in messages),
    )
    if not stats.content_size:
        logger.debug(f"Skipping {name!r}: empty")
        return
    if stats.authors_count < 3 and stats.reactions_count < 20:
        logger.debug(f"Skipping {name!r}: {stats!r}")
        return
    logger.info(f"Summarizing {name!r}: {stats!r}")
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(container="channel", items="messages")
    llm_response = await ask_for_json(system_prompt, serialize_messages(messages))
    summary = Summary(**llm_response)
    logger.info(f"Summarized {name!r}: {summary!r}")
    return ChannelSummary(stats=stats, summary=summary)


def serialize_messages(messages: list[ClubMessage]) -> str:
    return "\n\n---\n\n".join(
        [
            f"Message #{message.id} by user <@{message.author.id}>:\n\n{message.content}"
            for message in messages
        ]
    )


def serialize_channel_summaries(channel_summaries: Iterable[ChannelSummary]) -> str:
    return "\n\n---\n\n".join(
        [
            (
                f"Channel #{n} has "
                f"{channel_summary.stats.messages_count} new messages "
                f"by {channel_summary.stats.authors_count} users "
                f"({channel_summary.stats.content_size} characters "
                f"and {channel_summary.stats.reactions_count} emoji reactions total):\n\n"
                f"{channel_summary.summary.text}\n\n"
                f"Notable Topics:\n\n"
            )
            + "\n".join(
                f"- {topic.name} (Message ID: {topic.message_id})"
                for topic in channel_summary.summary.topics
            )
            for n, channel_summary in enumerate(channel_summaries, start=1)
        ]
    )
