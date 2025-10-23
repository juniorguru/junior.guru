import asyncio
import json
import re
from collections import Counter
from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter
from pprint import pformat

import click
from pydantic import BaseModel, conint, field_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers, months
from jg.coop.lib.cache import cache
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.llm import LLMModel, ask_llm
from jg.coop.models.base import SQLITE_INT_MAX, SQLITE_INT_MIN, db
from jg.coop.models.club import ClubChannel, ClubMessage, ClubSummaryTopic


logger = loggers.from_path(__file__)


class LLMTopic(BaseModel):
    engagement_score: int
    message_id: conint(ge=SQLITE_INT_MIN, le=SQLITE_INT_MAX)  # type: ignore
    name: str
    text: str


class LLMSummary(BaseModel):
    topics: list[LLMTopic]


class LLMTopicEmoji(BaseModel):
    topic_id: int
    emoji: str


class LLMTopicEmojis(BaseModel):
    items: list[LLMTopicEmoji]

    @field_validator("items")
    @classmethod
    def validate_items(cls, value: list[LLMTopicEmoji]) -> list[LLMTopicEmoji]:
        emoji_counts = Counter(item.emoji for item in value)
        duplicate_emojis = [emoji for emoji, count in emoji_counts.items() if count > 1]
        if duplicate_emojis:
            raise ValueError(f"Duplicate emojis found: {duplicate_emojis}")
        return value


class Topic(BaseModel):
    name: str
    text: str
    emoji: str
    message_id: int


class Summary(BaseModel):
    topics: list[Topic]


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--correction-attempts", default=3, type=int)
@db.connection_context()
@async_command
async def main(today: date, correction_attempts: int):
    logger.info("Setting up club topics db table")
    ClubSummaryTopic.drop_table()
    ClubSummaryTopic.create_table()

    logger.info("Summarizing club content")
    result = await summarize_club(today, correction_attempts)

    logger.info(f"Saving {len(result.topics)} topics")
    for order, topic in enumerate(result.topics, start=1):
        message = ClubMessage.get_by_id(topic.message_id)
        logger.debug(f"Topic {message.url}\n{pformat(topic.model_dump())}")
        ClubSummaryTopic.create(
            order=order,
            name=topic.name,
            text=topic.text,
            emoji=topic.emoji,
            message=message,
        )


@cache(expire=timedelta(days=1), tag="summary")
async def summarize_club(today: date, correction_attempts: int) -> Summary:
    prev_month = months.prev_month(today)
    logger.info(f"Summarizing since: {prev_month}")
    channel_mapping = ClubChannel.names_mapping()
    messages = ClubMessage.summary_listing(
        since_on=prev_month,
        exclude_channels=[
            ClubChannelID.GUIDE_DASHBOARD,
            ClubChannelID.GUIDE_EVENTS,
            ClubChannelID.GUIDE_ROLES,
            ClubChannelID.GUIDE_SPONSORS,
            ClubChannelID.VENTING,
            ClubChannelID.META,
        ],
        include_channels=[
            ClubChannelID.GROUPS,
            ClubChannelID.QA,
            ClubChannelID.ADVENTOFCODE,
            ClubChannelID.FUN_TOPICS,
        ],
    )

    logger.info(f"Serializing {len(messages)} messages to a text feed")
    feed = to_feed(
        list(messages),
        channel_mapping,
        threads_only_channels=[ClubChannelID.INTRO, ClubChannelID.TIL],
    )

    logger.info(f"Summarizing the feed, {len(feed)} characters… (takes a while)")
    summary = await ask_llm(
        """
            Pomáháš sledovat, co se děje v naší komunitě IT juniorů, která je na Discordu a říká si „klub“. Přijde ti přehled kanálů a zpráv. Ty uděláš shrnutí toho nejpodstatnějšího. Podstatná témata poznáš podle toho, že jsme si o nich hodně psali, zapojilo se do debaty víc členů, nebo to mělo dost (emoji) reakcí. Na výstupu vrať JSON s tématy, kde každé má čtyři atributy:

            - `topics` (array[object]): Seznam 15 nejpodstatnějších témat. Seřaď je od nejzásadnějších po ty méně významné. Každé téma obsahuje:
                - `engagement_score` (int): Skóre toho, jak bylo téma podstatné. Vypočítá se jako součet počtu zpráv, unikátních autorů a reakcí. Čím vyšší, tím lépe.
                - `message_id` (int): ID první zprávy, která to téma odstartovala.
                - `name` (string): Krátký název vystihující podstatu tématu. Bez slova „diskuze“ aj. zbytečností. NE: „Nahradí AI programátory?” NE: „Diskuze o AI” ANO: „Zkušenosti s nástroji na vibe coding”
                - `text` (string): Shrnutí tématu. Trochu jako „executive summary”, max 1800 znaků. Bez emotivních hodnocení. Jen fakta, názory, co jsme řešili a co lidi sdíleli. Nepiš úvod ani závěr. Vynech celkové hodnocení, jak na tebe diskuze působily a jaká se ti zdála atmosféra. Nezmiňuj v jaké části klubu (v jakých kanálech) jsme co probírali. Nepoužívej žádné formulace typu „hodně se řešilo“, „výrazná část konverzace“, „rozvinula se debata“, „populární téma bylo“, „nejvíc se mluvilo o“ apod. Napiš to bez jakéhokoli hodnocení četnosti, důležitosti nebo rozsahu témat. Nehodnoť ani nepřibližuj, kolik jsme toho psali. Prostě popiš jen obsah, ne kolik nebo jak moc.

            Důležité:
            - Nevymýšlej si ID zpráv.
            - Vše česky.
            - Témata se nesmí opakovat.
            - Přemýšlej nad tím krok za krokem.
        """,
        feed,
        model=LLMModel.advanced,
        schema=LLMSummary,
    )
    logger.info(f"The summary contains {len(summary.topics)} topics")
    logger.debug(f"Summary:\n{pformat(summary.model_dump())}")

    logger.info("Filtering out low-engagement topics")
    if len(summary.topics) < 10:
        raise ValueError("The summary contains less than 10 topics!")
    summary.topics = summary.topics[:10]

    for attempt in range(correction_attempts):
        logger.info(f"Verifying message IDs, attempt #{attempt + 1}")
        messages_existence = ClubMessage.check_existence(
            [topic.message_id for topic in summary.topics]
        )
        invalid_ids = [
            message_id
            for message_id, exists in messages_existence.items()
            if not exists
        ]
        if invalid_ids:
            logger.warning(f"Found {len(invalid_ids)} invalid message IDs")
            correction_prompt = f"""
                Toto je shrnutí toho nejpodstatnějšího, co se událo v naší Discord komunitě:

                {json.dumps(summary.model_dump(), indent=2, ensure_ascii=False)}

                Je v něm ale chyba. Shrnutí má obsahovat vždy ID první zprávy, která téma odstartovala. Jenže zprávy s těmito ID neexistují: {", ".join(map(str, invalid_ids))}

                Najdi v přiloženém přehledu kanálů a zpráv nějaké vhodné existující zprávy pro témata s chybnými ID, a nahraď chybná ID za čísla těchto zpráv.
                Důležité: Nic jiného ve shrnutí neměň, pouze oprav ta neexistující ID!
            """
            corrected_summary = await ask_llm(
                correction_prompt, feed, model=LLMModel.advanced, schema=LLMSummary
            )
            logger.debug(
                f"Corrected summary:\n{pformat(corrected_summary.model_dump())}"
            )
            invalid_topic_indexes_by_name = {
                topic.name: i
                for i, topic in enumerate(summary.topics)
                if topic.message_id in invalid_ids
            }
            for corrected_topic in corrected_summary.topics:
                try:
                    index = invalid_topic_indexes_by_name[corrected_topic.name]
                    logger.info(
                        f"Updating message ID for '{corrected_topic.name}': "
                        f"{summary.topics[index].message_id} → {corrected_topic.message_id}"
                    )
                    summary.topics[index].message_id = corrected_topic.message_id
                except KeyError:
                    logger.debug(
                        f"Topic '{corrected_topic.name}' not invalid, skipping"
                    )
        else:
            logger.info("All message IDs are valid!")
            break

    logger.info("Adjusting the summary text's style")
    tasks = [
        ask_llm(
            """
                Uprav následující český odstavec tak, aby byl čtivý a přirozený – jako když to někomu vyprávíš u kafe v práci.

                - Zestručni to zhruba do jedné věty, max 200 znaků. Zaměř se na hlavní myšlenky. Vynech detaily a konkrétní příklady.
                - Můžeš psát jako bys byl jedním z členů klubu, třeba „probrali jsme”, „řešili jsme”, „probírali jsme”, ale přirozeně to střídej s „řešilo se”, „probralo se”, „členové psali”, „lidi psali”, a tak. Občas se může hodit „prý”. NE: „Diskutovali jsme, že se AI nahradí programátory” ANO: „Prý AI nahradí programátory”.
                - Pokud mluvíš o účastnících diskuze, tak ANO: „lidi”, „členové klubu”, NE: „uživatelé”, „diskutující”.
                - Piš v minulém čase.
                - Žádné úvody, shrnutí, ani závěry navíc.
                - Pokud první věta pouze opakuje název tématu, tak ji vynech.
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
        schema=LLMTopicEmojis,
    )
    emojis = [item.emoji for item in emojis.items]
    logger.debug(f"Emojis:\n{pformat(emojis)}")

    return Summary(
        topics=[
            Topic(
                name=topic.name,
                text=topic.text,
                emoji=emojis[i],
                message_id=topic.message_id,
            )
            for i, topic in enumerate(summary.topics)
        ]
    )


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
        try:
            name = channel_mapping[channel_id]
        except KeyError:
            name = f"kanál-{channel_id}"
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
