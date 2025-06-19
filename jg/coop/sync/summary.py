import asyncio
import json
import re
from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter
from pprint import pformat

import click
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.llm import LLMModel, ask_llm
from jg.coop.models.base import db
from jg.coop.models.club import ClubChannel, ClubMessage


logger = loggers.from_path(__file__)


class Topic(BaseModel):
    engagement_score: int
    message_id: int
    name: str
    text: str


class Summary(BaseModel):
    topics: list[Topic]


class TopicEmoji(BaseModel):
    topic_id: int
    emoji: str


class TopicEmojis(BaseModel):
    items: list[TopicEmoji]


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
    channel_mapping = ClubChannel.names_mapping()
    messages = ClubMessage.summary_listing(
        since_on=since_on,
        exclude_channels=[
            ClubChannelID.GUIDE_DASHBOARD,
            ClubChannelID.GUIDE_EVENTS,
            ClubChannelID.GUIDE_ROLES,
            ClubChannelID.GUIDE_SPONSORS,
            ClubChannelID.VENTING,
            ClubChannelID.META,
        ],
        include_channels=[
            ClubChannelID.ADVENTOFCODE,
            ClubChannelID.FUN_TOPICS,
            ClubChannelID.QA,
        ],
    )

    logger.info(f"Serializing {len(messages)} messages to a text feed")
    feed = to_feed(
        list(messages),
        channel_mapping,
        threads_only_channels=[ClubChannelID.INTRO, ClubChannelID.TIL],
    )
    return  # TODO

    logger.info(f"Summarizing the feed, {len(feed)} characters… (takes a while)")
    summary = await ask_llm(
        """
            Pomáháš sledovat, co se děje v naší komunitě IT juniorů, která je na Discordu a říká si „klub“. Přijde ti přehled kanálů a zpráv. Ty uděláš shrnutí toho nejpodstatnějšího. Podstatná témata poznáš podle toho, že jsme si o nich hodně psali, zapojilo se do debaty víc členů, nebo to mělo dost (emoji) reakcí. Podobná témata nebo delší diskuze ale spoj, ať je ten výběr pestrý, ne že z jedné konverzace uděláš hned několik témat. Na výstupu vrať JSON s tématy, kde každé má čtyři atributy:

            - `topics` (array[object]): Seznam 15 nejpodstatnějších témat. Seřaď je od nejzásadnějších po ty méně významné. Každé téma obsahuje:
                - `engagement_score` (int): Skóre toho, jak bylo téma podstatné. Vypočítá se jako součet počtu zpráv, unikátních autorů a reakcí. Čím vyšší, tím lépe.
                - `message_id` (int): ID první zprávy, která to téma odstartovala.
                - `name` (string): Krátký název vystihující podstatu tématu. Bez slova „diskuze“ aj. zbytečností. NE: „Nahradí AI programátory?” NE: „Diskuze o AI” ANO: „Zkušenosti s nástroji na vibe coding”
                - `text` (string): Shrnutí tématu. Trochu jako „executive summary”, max 1800 znaků. Bez emotivních hodnocení. Jen fakta, názory, co jsme řešili a co lidi sdíleli. Nepiš úvod ani závěr. Vynech celkové hodnocení, jak na tebe diskuze působily a jaká se ti zdála atmosféra. Nezmiňuj v jaké části klubu (v jakých kanálech) jsme co probírali. Nepoužívej žádné formulace typu „hodně se řešilo“, „výrazná část konverzace“, „rozvinula se debata“, „populární téma bylo“, „nejvíc se mluvilo o“ apod. Napiš to bez jakéhokoli hodnocení četnosti, důležitosti nebo rozsahu témat. Nehodnoť ani nepřibližuj, kolik jsme toho psali. Prostě popiš jen obsah, ne kolik nebo jak moc.

            Důležité:
            - Nevymýšlej si ID zpráv.
            - Vše česky.
            - Přemýšlej nad tím krok za krokem.
        """,
        feed,
        model=LLMModel.advanced,
        schema=Summary,
    )
    logger.info(f"The summary contains {len(summary.topics)} topics")
    logger.debug(f"Summary:\n{pformat(summary.model_dump())}")

    logger.info("Filtering out low-engagement topics")
    summary.topics = summary.topics[:10]

    logger.info("Verifying message IDs")  # TODO prompt the LLM for correction
    for topic in summary.topics:
        ClubMessage.get_by_id(topic.message_id)

    logger.info("Adjusting the summary text's style")
    tasks = [
        ask_llm(
            """
                Uprav následující český odstavec tak, aby byl čtivý a přirozený – jako když to někomu vyprávíš u kafe v práci.

                - Zestručni to do pár vět, max 500 znaků. Zaměř se na hlavní myšlenky. Vynech detaily a konkrétní příklady.
                - Můžeš psát jako bys byl jedním z členů klubu, třeba „řešili jsme”, „probrali jsme”, „probírali jsme”, ale přirozeně to střídej s „řešilo se”, „probralo se”, „členové psali”, „lidi psali”, a tak. Občas se může hodit „prý”. NE: „Diskutovali jsme, že se AI nahradí programátory” ANO: „Prý AI nahradí programátory”.
                - Pokud mluvíš o účastnících diskuze, tak ANO: „lidi”, „členové klubu”, NE: „uživatelé”, „diskutující”.
                - Piš v minulém čase.
                - Žádné úvody, shrnutí, ani závěry navíc.
                - Nepiš nespisovně, ale piš přirozeně. Věty mohou být krátké, hlavně aby se dobře četly.
                - Dvakrát zkontroluj, že si nevymýšlíš žádné informace navíc. Uprav jen formu, ne obsah. Fakta a názvy musí sedět s původním textem.
            """,
            topic.text,
            model=LLMModel.advanced,
        )
        for topic in summary.topics
    ]
    for i, text in enumerate(await asyncio.gather(*tasks)):
        summary.topics[i].text = text.strip()
    logger.debug(f"Summary:\n{pformat(summary.model_dump())}")

    logger.info("Assigning emojis")
    emojis = await ask_llm(
        """
            To each topic in the JSON assign a single emoji that represents the topic. The emoji should be relevant to the topic and should not be too generic. The emojis must be unique accross the JSON. For each topic use only one emoji, not a combination of emojis.
        """,
        json.dumps(
            {
                "topics": [
                    {"topic_id": n, "content": f"{topic.name}: {topic.text}"}
                    for n, topic in enumerate(summary.topics, start=1)
                ]
            },
            indent=2,
            ensure_ascii=False,
        ),
        schema=TopicEmojis,
    )
    emojis = [item.emoji for item in emojis.items]
    logger.debug(f"Emojis:\n{pformat(emojis)}")


def to_feed(
    messages: list[ClubMessage],
    channel_mapping: dict[int, str],
    threads_only_channels: list[int] = None,
) -> str:
    docs = []
    for channel_id, channel_messages in groupby(messages, key=attrgetter("channel_id")):
        # some channels are only for threads, so we skip the top-level discussion
        if threads_only_channels and channel_id in threads_only_channels:
            continue

        # add starting message if it's in the selected period
        channel_messages = list(channel_messages)
        channel_messages = [
            m for m in messages if m.id == channel_id and m.id != channel_messages[0].id
        ] + channel_messages

        # stats
        messages_count = len(channel_messages)
        authors_count = len(set(m.author.id for m in channel_messages))
        reactions_count = sum(sum(m.reactions.values()) for m in channel_messages)
        content_size = sum(m.content_size for m in channel_messages)

        # skip low engagement channels
        if (
            messages_count < 10
            and authors_count < 10
            and reactions_count < 30
            and content_size < 10000
        ):
            logger.debug(f"Skipping channel: {channel_mapping[channel_id]}")
            continue

        logger.debug(f"Adding channel: {channel_mapping[channel_id]}")
        channel_header = (
            f"Kanál <#{channel_id}> má "
            f"{messages_count} nových příspěvků "
            f"od {authors_count} členů "
            f"(celkem písmen {content_size}, "
            f"emoji reakcí {reactions_count})"
        )
        docs.append(f"\n\n{channel_header.upper()}:")
        for message in channel_messages:
            reactions = ", ".join(
                f"{count}×{f':{emoji}:' if re.search(r'^[a-zA-Z0-9]+$', emoji) else emoji}"
                for emoji, count in message.reactions.items()
            )
            reactions = f", reakce {reactions}" if reactions else ""
            doc = (
                f"[Příspěvek #{message.id} od člena <@{message.author.id}>{reactions}]\n"
                f"{message.content}"
            )
            docs.append(doc)
    text = "\n---\n".join(docs)
    text = simplify_channel_mentions(text, channel_mapping)
    text = simplify_member_mentions(text)
    text = simplify_custom_emojis(text)
    return text


def simplify_channel_mentions(text: str, channel_mapping: dict[int, str]) -> str:
    for match in re.finditer(r"<#!?(\d+)>", text):
        channel_id = int(match.group(1))
        name = channel_mapping[channel_id]
        name_repr = f"#{name}" if re.search(r"^[\w\-]+$", name) else f"<#{name}>"
        text = text.replace(match.group(0), name_repr)
    return text


def simplify_member_mentions(text: str) -> str:
    user_ids = []
    for match in re.finditer(r"<@!?(\d+)>", text):
        user_id = int(match.group(1))
        try:
            index = user_ids.index(user_id)
        except ValueError:
            user_ids.append(user_id)
            index = len(user_ids) - 1
        text = text.replace(match.group(0), f"@member{index + 1}")
    return text


def simplify_custom_emojis(text: str) -> str:
    return re.sub(r"<a?:([^:]+):\d+>", r":\1:", text)
