import json
import re
from datetime import date, datetime, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Any

import click
import discord
import extruct
import ics
import requests
from juniorguru_chick.lib.threads import create_thread, ensure_thread_name
from lxml import html

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers, mutations
from juniorguru.lib.discord_club import ClubClient, ClubMemberID, parse_channel
from juniorguru.lib.locations import fetch_location
from juniorguru.models.club import ClubMessage


NAME_PREFIX = 'Mini sraz juniorů'

MEETUP_URL_RE = re.compile(r'https?://\S+', re.IGNORECASE)

CALL_TO_ACTION_TEXT = (
    'Chceš se poznat s lidmi z klubu i naživo? '
    'Běžně se potkáváme na srazech vybraných komunit. '
    'Utvořte skupinku, ničeho se nebojte, a vyrazte!'
)

IMAGES_DIR = Path('juniorguru/images')

FEEDS = [
    dict(slug='pyvo',
         emoji='<:python:842331892091322389>',
         name=f'{NAME_PREFIX} na akci pythonistů (Pyvo)',
         poster_path='posters-meetups/pyvo.png',
         format='icalendar',
         source_url='https://pyvo.cz/api/pyvo.ics'),
    dict(slug='pydata',
         emoji='<:pydata:1136778714521272350>',
         name=f'{NAME_PREFIX} na akci datařů (PyData)',
         poster_path='posters-meetups/pydata.png',
         format='meetup_com',
         source_url='https://www.meetup.com/pydata-prague/'),
    dict(slug='reactgirls',
         emoji='<:react:842332165822742539>',
         name=f'{NAME_PREFIX} na akci React Girls',
         poster_path='posters-meetups/reactgirls.png',
         format='meetup_com',
         source_url='https://www.meetup.com/reactgirls/events/'),
    dict(slug='frontendisti',
         emoji='<:frontendisti:900831766644944936>',
         name=f'{NAME_PREFIX} na akci frontendistů',
         poster_path='posters-meetups/frontendisti.png',
         format='meetup_com',
         source_url='https://www.meetup.com/frontendisti/events/'),
    dict(slug='pehapkari',
         emoji='<:php:842331754731274240>',
         name=f'{NAME_PREFIX} na akci péhápkářů',
         poster_path='posters-meetups/pehapkari.png',
         format='meetup_com',
         source_url='https://www.meetup.com/pehapkari/'),
]

USER_AGENT = 'JuniorGuruBot (+https://junior.guru)'

TIMELINE_LIMIT_DAYS = 60

EVENT_EMOJI = '📅'


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content'])
@click.option('--channel', 'channel_id', default='promo', type=parse_channel)
@click.option('--clear-cache/--keep-cache', default=False)
@click.pass_context
def main(context, channel_id, clear_cache):
    cache_path = context.obj['cache_dir'] / 'meetups.json'
    if clear_cache:
        cache_path.unlink(missing_ok=True)
    try:
        logger.info('Loading data from cache')
        data = json.loads(cache_path.read_text())
    except FileNotFoundError:
        logger.debug('No cache found')
        data = []
        for feed in FEEDS:
            logger.info(f'Downloading {feed["format"]!r} feed from {feed["source_url"]}')
            response = requests.get(feed['source_url'], headers={'User-Agent': USER_AGENT})
            response.raise_for_status()
            feed['source_url'] = response.url  # overwrite with the final URL
            feed['data'] = response.text
            data.append(feed)
        logger.info('Caching data')
        cache_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    logger.info('Parsing events')
    today = date.today()
    events = []
    for feed in data:
        if feed['format'] == 'icalendar':
            events.extend([dict(**feed, **event_data)
                           for event_data in parse_icalendar(feed['data'])])
        elif feed['format'] == 'meetup_com':
            events.extend([dict(**feed, **event_data)
                           for event_data in parse_meetup_com(feed['data'])])
        elif feed['format'] == 'json-dl':  # currently not needed, remove in the future if unused
            events.extend([dict(**feed, **event_data)
                           for event_data in parse_json_dl(feed['data'], feed['source_url'])])
        else:
            raise ValueError(f"Unknown feed format {feed['format']!r}")

    logger.info('Filtering and sorting events')
    timeline_limit = today + timedelta(days=TIMELINE_LIMIT_DAYS)
    events = sorted((event for event in events
                     if (event['starts_at'].date() > today)
                         and event['starts_at'].date() <= timeline_limit),
                    key=itemgetter('starts_at'))

    logger.info('Processing location')
    for event in events:
        logger.debug(f"Locating: {event['name_raw']}")
        event['location'] = fetch_location(event['location_raw'])

    logger.info(f'Syncing {len(events)} with Discord, using channel #{channel_id}')
    discord_sync.run(sync_events, events, channel_id)


@mutations.mutates_discord()
async def sync_events(client: ClubClient, events: list[dict], channel_id: int):
    discord_events = {parse_meetup_url(scheduled_event.description): scheduled_event
                      for scheduled_event in client.club_guild.scheduled_events
                      if is_meetup_scheduled_event(scheduled_event)}
    discord_channel = await client.fetch_channel(channel_id)

    for event in events:
        try:
            discord_event = discord_events.pop(event['url'])
        except KeyError:
            logger.info(f"Creating Discord event: {event['name']!r}, {event['url']}")
            discord_event = await client.club_guild.create_scheduled_event(
                image=(IMAGES_DIR / event['poster_path']).read_bytes(),
                **generate_scheduled_event(event),
            )
        else:
            logger.info(f"Updating Discord event: {event['name']!r}, {event['url']}")
            discord_event = await discord_event.edit(
                cover=(IMAGES_DIR / event['poster_path']).read_bytes(),
                **generate_scheduled_event(event),
            )

        logger.info("Ensuring channel message")
        if channel_message := ClubMessage.last_bot_message(channel_id,
                                                           starting_emoji=EVENT_EMOJI,
                                                           contains_text=event['url']):
            logger.debug(f'Channel message already exists: {channel_message.url}')
            discord_channel_message = await discord_channel.fetch_message(channel_message.id)
        else:
            logger.info('Could not find channel message, posting')
            discord_channel_message = await discord_channel.send(generate_channel_message_content(event))

        logger.info("Ensuring thread exists")
        if discord_channel_message.flags.has_thread:
            logger.debug("Thread already exists")
            thread = await discord_channel_message.guild.fetch_channel(discord_channel_message.id)
        else:
            logger.info("Creating thread")
            thread = await create_thread(discord_channel_message, thread_name(event))

        if thread.archived or thread.locked:
            logger.warning(f"Thread {discord_channel_message.jump_url} is archived or locked, skipping")
            continue

        logger.debug(f"Ensuring correct thread name for {discord_channel_message.author.display_name!r}")
        await ensure_thread_name(thread, thread_name(event))

        logger.info("Ensuring thread message")
        mentions = [user.mention async for user in discord_event.subscribers()]
        message_content = generate_thread_message_content(discord_event.url, mentions)
        if thread_message := ClubMessage.last_bot_message(thread.id, contains_text=discord_event.url):
            logger.debug(f'Thread message already exists: {thread_message.url}')
            discord_thread_message = await thread.fetch_message(thread_message.id)
            if discord_thread_message.content != message_content:
                logger.info('Updating thread message')
                await discord_thread_message.edit(content=message_content)
            else:
                logger.debug('Thread message is up-to-date')
        else:
            logger.info('Could not find thread message, posting')
            await thread.send(message_content)

    for discord_event in discord_events.values():
        logger.info(f"Canceling Discord event: {discord_event.name!r}, {discord_event.url}")
        await discord_event.cancel()


def parse_icalendar(content: str) -> list[dict[str, Any]]:
    return [dict(name_raw=event.summary,
                 starts_at=event.begin,
                 location_raw=event.location,
                 url=event.url)
            for event in ics.Calendar(content).events
            if 'tentative-date' not in event.categories]


# currently not needed, remove in the future if unused
def parse_json_dl(content: str, base_url: str) -> list[dict[str, Any]]:
    data = extruct.extract(content, base_url, syntaxes=['json-ld'])
    return [dict(name_raw=item['name'],
                 starts_at=datetime.fromisoformat(item['startDate']),
                 location_raw=parse_json_dl_location(item['location']),
                 url=item['url'])
            for item in data['json-ld']
            if item['@type'] == 'Event' and base_url in item['url']]


# currently not needed, remove in the future if unused
def parse_json_dl_location(location: dict[str, str]) -> str:
    return f"{location['name']}, {location['address']['streetAddress']}, {location['address']['addressLocality']}, {location['address']['addressCountry']}"


def parse_meetup_com(content: str) -> list[dict[str, Any]]:
    html_tree = html.fromstring(content)
    next_data = json.loads(html_tree.cssselect('#__NEXT_DATA__')[0].text_content())
    apollo_state = next_data['props']['pageProps']['__APOLLO_STATE__']
    venues = {key: venue
              for key, venue
              in apollo_state.items()
              if key.startswith('Venue:')}
    return [dict(name_raw=event['title'],
                 starts_at=datetime.fromisoformat(event['dateTime']),
                 location_raw=parse_meetup_com_location(venues[event['venue']['__ref']]),
                 url=event['eventUrl'])
            for key, event
            in apollo_state.items()
            if (key.startswith('Event:')
                and event['isOnline'] == False
                and event['eventType'] == 'PHYSICAL'
                and event['status'] == 'ACTIVE')]


def parse_meetup_com_location(location: dict[str, Any]) -> str:
    parts = [location['name'], location['address'], location['city'], location['state'], location['country'].upper()]
    return ", ".join(filter(None, parts))


def is_bot_message(discord_message: discord.Message) -> bool:
    return discord_message.type == discord.MessageType.default and discord_message.author.id == ClubMemberID.BOT


def is_meetup_scheduled_event(scheduled_event: discord.ScheduledEvent) -> bool:
    return int(scheduled_event.creator_id) == ClubMemberID.BOT and NAME_PREFIX in scheduled_event.name


def parse_meetup_url(text: str) -> str:
    return MEETUP_URL_RE.search(text).group(0)


def generate_scheduled_event(event: dict) -> dict:
    return dict(
        name=f"{event['location'][1]}: {event['name']}",
        description=(f'**Akce:** {event["name_raw"]}\n**Více info:** {event["url"]}\n\n{CALL_TO_ACTION_TEXT}'),
        start_time=event['starts_at'],
        end_time=event['starts_at'] + timedelta(hours=3),
        location=event['location_raw'],
    )


def generate_channel_message_content(event: dict) -> str:
    return (
        f"{EVENT_EMOJI} **{event['location'][1]}, {event['starts_at']:%-d.%-m.}**"
        "\n\n"
        f"{event['emoji']} Kdo se chystá na {event['name_raw']}? Zakládám vlákno!"
        "\n\n"
        f"{event['url']}"
    )


def thread_name(event: dict) -> str:
    return f"{event['location'][1]}, {event['starts_at']:%-d.%-m.} – {event['name_raw']}"


def generate_thread_message_content(scheduled_event_url: str, mentions: list[str] = None) -> str:
    text = CALL_TO_ACTION_TEXT
    if mentions:
        mentions = sorted(mentions or [])
        text += (
            "\n\n"
            "Už teď to vypadá, že na akci potkáš "
            f"{' '.join(mentions)}"
            "\n\n"
        )
    text += scheduled_event_url
    return text
