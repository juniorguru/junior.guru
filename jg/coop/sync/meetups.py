import json
import re
import textwrap
from datetime import date, datetime, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Any, Generator
from zoneinfo import ZoneInfo

import click
import discord
import ics
import requests
import teemup

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.cache import cache
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import (
    DEFAULT_AUTO_ARCHIVE_DURATION,
    ClubClient,
    ClubMemberID,
    fetch_threads,
    parse_channel,
)
from jg.coop.lib.mapycz import locate
from jg.coop.models.club import ClubMessage


NAME_PREFIX = "Mini sraz juniorů"

NAME_LENGTH_LIMIT = 100

LOCATION_LENGTH_LIMIT = 100

MEETUP_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)

CALL_TO_ACTION_TEXT = (
    "Chceš se poznat s lidmi z klubu i naživo? "
    "Běžně se potkáváme na srazech vybraných komunit. "
    "Utvořte skupinku, ničeho se nebojte, a vyrazte!"
)

IMAGES_DIR = Path("jg/coop/images")

USER_AGENT = "JuniorGuruBot (+https://junior.guru)"

USER_AGENT_MEETUP = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"

FEEDS = [
    dict(
        slug="pyvo",
        emoji="<:python:842331892091322389>",
        name=f"{NAME_PREFIX} na akci pythonistů",
        poster_path="posters-meetups/pyvo.png",
        format="icalendar",
        source_url="https://pyvo.cz/api/pyvo.ics",
        user_agent=USER_AGENT,
    ),
    dict(
        slug="pydata",
        emoji="<:pydata:1136778714521272350>",
        name=f"{NAME_PREFIX} na akci datařů",
        poster_path="posters-meetups/pydata.png",
        format="meetup_com",
        source_url="https://www.meetup.com/pydata-prague/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="reactgirls",
        emoji="<:react:842332165822742539>",
        name=f"{NAME_PREFIX} na akci reakťaček",
        poster_path="posters-meetups/reactgirls.png",
        format="meetup_com",
        source_url="https://www.meetup.com/reactgirls/events/",
        user_agent=USER_AGENT_MEETUP,
        skip=["workshop", "canvas:"],
    ),
    dict(
        slug="frontendisti",
        emoji="<:frontendisti:900831766644944936>",
        name=f"{NAME_PREFIX} na akci frontendistů",
        poster_path="posters-meetups/frontendisti.png",
        format="meetup_com",
        source_url="https://www.meetup.com/frontendisti/events/",
        user_agent=USER_AGENT_MEETUP,
        skip=["konference"],
    ),
    dict(
        slug="pehapkari",
        emoji="<:php:842331754731274240>",
        name=f"{NAME_PREFIX} na akci péhápkářů",
        poster_path="posters-meetups/pehapkari.png",
        format="meetup_com",
        source_url="https://www.meetup.com/pehapkari/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="pehapkari-brno",
        emoji="<:php:842331754731274240>",
        name=f"{NAME_PREFIX} na akci péhápkářů",
        poster_path="posters-meetups/pehapkari.png",
        format="meetup_com",
        source_url="https://www.meetup.com/pehapkari-brno/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="ctvrtkon",
        emoji="🍻",
        name=f"{NAME_PREFIX} na akci jihočeské tech komunity",
        poster_path="posters-meetups/ctvrtkon.png",
        format="ctvrtkon",
        source_url="https://ctvrtkon.cz/api/events/feed",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="czechtesters",
        emoji="🍻",
        name=f"{NAME_PREFIX} na akci testerů",
        poster_path="posters-meetups/czechtesters.png",
        format="meetup_com",
        source_url="https://www.meetup.com/professionaltesting/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="protest",
        emoji="🍻",
        name=f"{NAME_PREFIX} na akci testerů",
        poster_path="posters-meetups/protest.png",
        format="meetup_com",
        source_url="https://www.meetup.com/protest_cz/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="praguejs",
        emoji="<:javascript:842329110293381142>",
        name=f"{NAME_PREFIX} na akci javascripťáků",
        poster_path="posters-meetups/praguejs.png",
        format="meetup_com",
        source_url="https://www.meetup.com/praguejs/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
    dict(
        slug="techmeetup",
        emoji="🍻",
        name=f"{NAME_PREFIX} na akci ostravské tech komunity",
        poster_path="posters-meetups/techmeetup.png",
        format="meetup_com",
        source_url="https://www.meetup.com/techmeetupostrava/events/",
        user_agent=USER_AGENT_MEETUP,
        skip=["conference", "konference", "agile circle"],
    ),
    dict(
        slug="praguegenai",
        emoji="🤖",
        name=f"{NAME_PREFIX} na akci AI nadšenců",
        poster_path="posters-meetups/praguegenai.png",
        format="meetup_com",
        source_url="https://www.meetup.com/prague-gen-ai/events/",
        user_agent=USER_AGENT_MEETUP,
    ),
]

TIMELINE_LIMIT_DAYS = 60

TAG_NAME = "sraz"


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
@click.option("--channel", "channel_id", default="promo", type=parse_channel)
@async_command
async def main(channel_id):
    today = date.today()
    events = []
    for feed in fetch_feeds():
        if feed["format"] == "icalendar":
            events.extend(
                [
                    dict(**feed, **event_data)
                    for event_data in parse_icalendar(feed["data"])
                    if isnt_skipped(event_data, feed.get("skip"))
                ]
            )
        elif feed["format"] == "meetup_com":
            events.extend(
                [
                    dict(**feed, **event_data)
                    for event_data in parse_meetup_com(feed["data"])
                    if isnt_skipped(event_data, feed.get("skip"))
                ]
            )
        elif feed["format"] == "ctvrtkon":
            events.extend(
                [
                    dict(**feed, **event_data)
                    for event_data in parse_ctvrtkon(feed["data"])
                    if isnt_skipped(event_data, feed.get("skip"))
                ]
            )
        else:
            raise ValueError(f"Unknown feed format {feed['format']!r}")

    logger.info("Filtering and sorting events")
    timeline_limit = today + timedelta(days=TIMELINE_LIMIT_DAYS)
    events = sorted(
        (
            event
            for event in events
            if (event["starts_at"].date() > today)
            and event["starts_at"].date() <= timeline_limit
        ),
        key=itemgetter("starts_at"),
    )

    logger.info("Processing location")
    for event in events:
        logger.debug(f"Locating: {event['name_raw']}")
        event["location"] = await locate(event["location_raw"])

    logger.info(
        f"Syncing {len(events)} events with Discord, using channel #{channel_id}"
    )
    discord_task.run(sync_events, events, channel_id)


@cache(expire=timedelta(days=1), tag="meetups")
def fetch_feeds() -> list[dict]:
    logger.info("Fetching feeds")
    data = []
    for feed in FEEDS:
        logger.info(f'Downloading {feed["format"]!r} feed from {feed["source_url"]}')
        response = requests.get(feed["source_url"], headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        feed["source_url"] = response.url  # overwrite with the final URL
        feed["data"] = response.text
        data.append(feed)
    return data


@mutations.mutates_discord()
async def sync_events(client: ClubClient, events: list[dict], channel_id: int):
    discord_events = {
        parse_meetup_url(scheduled_event.description): scheduled_event
        for scheduled_event in client.club_guild.scheduled_events
        if is_meetup_scheduled_event(scheduled_event)
    }
    logger.info(f"Found {len(discord_events)} relevant scheduled events")

    discord_channel = await client.club_guild.fetch_channel(channel_id)
    discord_tag = [
        tag for tag in discord_channel.available_tags if tag.name == TAG_NAME
    ][0]
    posts = {
        parse_meetup_url(message.content): message
        for message in ClubMessage.channel_listing(channel_id, parent=True, by_bot=True)
        if message.is_starting_message
    }
    logger.info(f"Found {len(posts)} relevant forum posts")

    for event in events:
        try:
            discord_event = discord_events.pop(event["url"])
        except KeyError:
            logger.info(f"Creating Discord event: {event['name']!r}, {event['url']}")
            discord_event = await client.club_guild.create_scheduled_event(
                image=(IMAGES_DIR / event["poster_path"]).read_bytes(),
                **generate_scheduled_event(event),
            )
        else:
            logger.info(f"Updating Discord event: {event['name']!r}, {event['url']}")
            discord_event = await discord_event.edit(
                cover=(IMAGES_DIR / event["poster_path"]).read_bytes(),
                **generate_scheduled_event(event),
            )

        post_name = thread_name(event)
        post_content = generate_starting_message_content(event)
        try:
            post = posts.pop(event["url"])
        except KeyError:
            logger.info(f"Creating thread for {event['url']}")
            discord_thread = await discord_channel.create_thread(
                name=post_name,
                content=post_content,
                auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION,
                applied_tags=[discord_tag],
            )
        else:
            logger.info(f"Found thread for {event['url']}")
            discord_thread = discord_channel.get_thread(post.id)
            if not discord_thread:
                logger.warning(
                    f"Thread {post.url} not available, iterating over all threads to get its object"
                )
                async for thread in fetch_threads(discord_channel):
                    if thread.id == post.id:
                        discord_thread = thread
                        break
            if not discord_thread:
                raise ValueError(f"Could not find thread {post.url}")

            logger.info(f"Updating thread for {event['url']}")
            discord_thread = await discord_thread.edit(
                archived=False,
                name=post_name,
                auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION,
                applied_tags=[discord_tag],
            )
            discord_message = discord_thread.get_partial_message(discord_thread.id)
            await discord_message.edit(content=post_content)

        logger.info(f"Ensuring thread message for {event['url']}")
        mentions = [user.mention async for user in discord_event.subscribers()]
        thread_message_content = generate_thread_message_content(
            discord_event.url, mentions
        )
        if thread_message := ClubMessage.last_bot_message(
            discord_thread.id, contains_text=discord_event.url
        ):
            logger.debug(f"Thread message already exists: {thread_message.url}")
            discord_thread_message = await discord_thread.fetch_message(
                thread_message.id
            )
            if discord_thread_message.content != thread_message_content:
                logger.info("Updating thread message")
                await discord_thread_message.edit(content=thread_message_content)
            else:
                logger.debug("Thread message is up-to-date")
        else:
            logger.info("Could not find thread message, posting")
            await discord_thread.send(thread_message_content)

    for discord_event in discord_events.values():
        logger.info(
            f"Canceling Discord event: {discord_event.name!r}, {discord_event.url}"
        )
        await discord_event.cancel()


def isnt_skipped(event: dict[str, Any], skip: None | list[str] = None) -> bool:
    if not skip:
        return True
    return not any(skip in event["name_raw"].lower() for skip in skip)


def parse_icalendar(content: str) -> list[dict[str, Any]]:
    return [
        dict(
            name_raw=event.summary,
            starts_at=event.begin,
            location_raw=event.location,
            url=event.url,
        )
        for event in ics.Calendar(content).events
        if "tentative-date" not in event.categories
    ]


def parse_meetup_com(content: str) -> Generator[dict[str, Any], None, None]:
    for event in teemup.parse(content):
        if event["venue"]:
            try:
                location_raw = parse_meetup_com_location(event["venue"])
            except ValueError:
                pass  # skipping online events without location
            else:
                yield dict(
                    name_raw=event["title"],
                    starts_at=event["starts_at"],
                    location_raw=location_raw,
                    url=event["url"],
                )


def parse_meetup_com_location(venue: dict[str, Any] | None) -> str:
    if not venue:
        raise ValueError("Event without venue (e.g. online event)")
    parts = [
        venue["name"],
        venue["address"],
        venue["city"],
        venue["state"],
        venue["country"].upper(),
    ]
    return ", ".join(filter(None, parts))


def parse_ctvrtkon(content: str) -> list[dict[str, Any]]:
    return [
        dict(
            name_raw=event["name"],
            starts_at=datetime.fromisoformat(event["started_at"]).replace(
                tzinfo=ZoneInfo("Europe/Prague")
            ),
            location_raw=f"{event['venue']['name']}, {event['venue']['address']}",
            url=f"https://ctvrtkon.cz/public/udalost/{event['slug']}",
        )
        for event in json.loads(content)["data"]
    ]


def is_meetup_scheduled_event(scheduled_event: discord.ScheduledEvent) -> bool:
    # For some reason by October 2023 the creator_id is always None, probably bug on Discord's side.
    # Checking if it's created by the bot only if it's not None should be future proof.
    #
    # https://github.com/discord/discord-api-docs/issues/6481
    if (
        scheduled_event.creator_id is not None
        and int(scheduled_event.creator_id) != ClubMemberID.BOT
    ):
        return False
    return NAME_PREFIX in scheduled_event.name


def parse_meetup_url(text: str) -> str:
    return MEETUP_URL_RE.search(text).group(0)


def generate_scheduled_event(event: dict) -> dict:
    return dict(
        name=f"{event['location'].place}: {event['name']}",
        description=(
            f'**Akce:** {event["name_raw"]}\n**Více info:** {event["url"]}\n\n{CALL_TO_ACTION_TEXT}'
        ),
        start_time=event["starts_at"],
        end_time=event["starts_at"] + timedelta(hours=3),
        location=textwrap.shorten(
            event["location_raw"], width=LOCATION_LENGTH_LIMIT, placeholder="…"
        ),
    )


def thread_name(event: dict, limit=NAME_LENGTH_LIMIT) -> str:
    name = f"{event['location'].place}, {event['starts_at']:%-d.%-m.} – {event['name_raw']}"
    if len(name) >= limit:
        return name[: limit - 1] + "…"
    return name


def generate_thread_message_content(
    scheduled_event_url: str, mentions: list[str] = None
) -> str:
    text = CALL_TO_ACTION_TEXT
    if mentions:
        mentions = sorted(mentions)
        text += f"\n\nUž teď to vypadá, že na akci potkáš {' '.join(mentions)}\n\n"
    else:
        text += " "
    text += scheduled_event_url
    return text


def generate_starting_message_content(event: dict) -> str:
    return (
        f"Kdo se chystá na {event['name_raw']}? "
        f"{event['emoji']} "
        "Zakládám vlákno! "
        "Podrobnosti najdeš tady: "
        f"{event['url']}"
    )
