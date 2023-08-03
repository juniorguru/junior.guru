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

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib import mutations
from juniorguru.lib.discord_club import ClubClient, ClubMemberID, parse_channel
from juniorguru.lib.locations import fetch_location
from juniorguru.models.club import ClubMessage


NAME_PREFIX = 'Mini sraz juniorů'

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
         format='json-dl',
         source_url='https://www.meetup.com/pydata-prague/'),
    dict(slug='reactgirls',
         emoji='<:react:842332165822742539>',
         name=f'{NAME_PREFIX} na akci React Girls',
         poster_path='posters-meetups/reactgirls.png',
         format='json-dl',
         source_url='https://www.meetup.com/reactgirls/events/'),
    dict(slug='frontendisti',
         emoji='<:frontendisti:900831766644944936>',
         name=f'{NAME_PREFIX} na akci frontendistů',
         poster_path='posters-meetups/frontendisti.png',
         format='json-dl',
         source_url='https://www.meetup.com/frontendisti/events/'),
    dict(slug='pehapkari',
         emoji='<:php:842331754731274240>',
         name=f'{NAME_PREFIX} na akci péhápkářů',
         poster_path='posters-meetups/pehapkari.png',
         format='json-dl',
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
        elif feed['format'] == 'json-dl':
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
        event['location'] = fetch_location(event['location_raw'])

    logger.info(f'Syncing {len(events)} with Discord, using channel #{channel_id}')
    discord_sync.run(sync_events, events, channel_id)


@mutations.mutates_discord()
async def sync_events(client: ClubClient, events: list[dict], channel_id: int):
    discord_events = {re.search(r'https?://\S+', e.description).group(0): e
                      for e in client.club_guild.scheduled_events
                      if (int(e.creator_id) == ClubMemberID.BOT
                          and NAME_PREFIX in e.name)}
    discord_channel = await client.fetch_channel(channel_id)

    for event in events:
        params = dict(
            name=f"{event['location'][1]}: {event['name']}",
            description=(f'**Akce:** {event["name_raw"]}\n**Více info:** {event["url"]}\n\n'
                            'Chceš se poznat s lidmi z klubu i naživo? '
                            'Běžně se potkáváme na srazech vybraných komunit. '
                            'Utvořte skupinku, ničeho se nebojte, a vyražte!'),
            start_time=event['starts_at'],
            end_time=event['starts_at'] + timedelta(hours=3),
            location=event['location_raw'],
        )
        try:
            discord_event = discord_events.pop(event['url'])
        except KeyError:
            logger.info(f"Creating Discord event: {event['name']!r}, {event['url']}")
            await client.club_guild.create_scheduled_event(
                image=(IMAGES_DIR / event['poster_path']).read_bytes(),
                **params,
            )
        else:
            logger.info(f"Updating Discord event: {event['name']!r}, {event['url']}")
            discord_event = await discord_event.edit(
                cover=(IMAGES_DIR / event['poster_path']).read_bytes(),
                **params,
            )

        logger.info("Ensuring the channel message")
        if channel_message := ClubMessage.last_bot_message(channel_id,
                                                           starting_emoji=EVENT_EMOJI,
                                                           contains_text=event['url']):
            logger.debug(f'Channel message already exists: {channel_message.url}')
            discord_channel_message = await discord_channel.fetch_message(channel_message.id)
        else:
            logger.debug('Could not find channel message, posting')
            discord_channel_message = await discord_channel.send(
                f"{EVENT_EMOJI} **{event['location'][1]}, {event['starts_at']:%-d.%-m.}**"
                "\n\n"
                f"{event['emoji']} Kdo se chystá na {event['name_raw']}? Zakládám vlákno!"
                "\n\n"
                f"{event['url']}"
            )

        logger.info("Ensuring thread exists")
        thread_name = f"{event['location'][1]}, {event['starts_at']:%-d.%-m.} – {event['name_raw']}"
        if discord_channel_message.flags.has_thread:
            logger.debug("Thread already exists")
            thread = await discord_channel_message.guild.fetch_channel(discord_channel_message.id)
        else:
            logger.debug("Creating thread")
            thread = await create_thread(discord_channel_message, thread_name)

        if thread.archived or thread.locked:
            logger.warning(f"Thread {discord_channel_message.jump_url} is archived or locked, skipping")
            continue

        logger.debug(f"Ensuring correct thread name for {discord_channel_message.author.display_name!r}")
        await ensure_thread_name(thread, thread_name)

        logger.debug("Ensuring the thread message")
        message_content = (
            'Chceš se poznat s lidmi z klubu i naživo? '
            'Běžně se potkáváme na srazech vybraných komunit. '
            'Utvořte skupinku, ničeho se nebojte, a vyražte! '
        )
        mentions = sorted([user.mention async for user in discord_event.subscribers()])
        if mentions:
            message_content += (
                "\n\nUž teď to vypadá, že na akci potkáš "
                f"{' '.join(mentions)}\n\n"
            )
        message_content += discord_event.url
        if thread_message := ClubMessage.last_bot_message(thread.id, contains_text=discord_event.url):
            logger.debug(f'Thread message already exists: {thread_message.url}')
            discord_thread_message = await thread.fetch_message(thread_message.id)
            if discord_thread_message.content != message_content:
                logger.debug('Updating thread message')
                await discord_thread_message.edit(content=message_content)
            else:
                logger.debug('Thread message is up-to-date')
        else:
            logger.debug('Could not find thread message, posting')
            await thread.send(message_content)

    for discord_event in discord_events.values():
        logger.info(f"Canceling Discord event: {discord_event.name!r}, {discord_event.url}")
        await discord_event.cancel()


def parse_icalendar(text: str) -> list[dict[str, Any]]:
    return [dict(name_raw=event.summary,
                 starts_at=event.begin,
                 location_raw=event.location,
                 url=event.url)
            for event in ics.Calendar(text).events
            if 'tentative-date' not in event.categories]


def parse_json_dl(html: str, base_url: str) -> list[dict[str, Any]]:
    data = extruct.extract(html, base_url, syntaxes=['json-ld'])
    return [dict(name_raw=item['name'],
                 starts_at=datetime.fromisoformat(item['startDate']),
                 location_raw=parse_json_dl_location(item['location']),
                 url=item['url'])
            for item in data['json-ld']
            if item['@type'] == 'Event' and base_url in item['url']]


def parse_json_dl_location(location: dict[str, str]) -> str:
    return f"{location['name']}, {location['address']['streetAddress']}, {location['address']['addressLocality']}, {location['address']['addressCountry']}"


def is_bot_message(discord_message: discord.Message) -> bool:
    return discord_message.type == discord.MessageType.default and discord_message.author.id == ClubMemberID.BOT
