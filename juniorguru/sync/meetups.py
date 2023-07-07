import json
import re
from datetime import date, datetime, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Any

import click
import extruct
import ics
import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import ClubMemberID
from juniorguru.lib.locations import fetch_location
from juniorguru.lib.mutations import mutating_discord


NAME_PREFIX = 'Mini sraz juniorů'

IMAGES_DIR = Path('juniorguru/images')

FEEDS = [
    dict(slug='pyvo',
         name=f'{NAME_PREFIX} na akci pythonistů (Pyvo)',
         poster_path='posters-meetups/pyvo.png',
         format='icalendar',
         source_url='https://pyvo.cz/api/pyvo.ics'),
    dict(slug='reactgirls',
         name=f'{NAME_PREFIX} na akci React Girls',
         poster_path='posters-meetups/reactgirls.png',
         format='json-dl',
         source_url='https://www.meetup.com/reactgirls/events/'),
    dict(slug='frontendisti',
         name=f'{NAME_PREFIX} na akci frontendistů',
         poster_path='posters-meetups/frontendisti.png',
         format='json-dl',
         source_url='https://www.meetup.com/frontendisti/events/'),
]

USER_AGENT = 'JuniorGuruBot (+https://junior.guru)'

TIMELINE_LIMIT_DAYS = 60


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--clear-cache/--keep-cache')
@click.pass_context
def main(context, clear_cache):
    logger.info('Reading cache')
    cache_path = context.obj['cache_dir'] / 'meetups.json'
    if clear_cache:
        cache_path.unlink(missing_ok=True)
    try:
        data = json.loads(cache_path.read_text())
    except FileNotFoundError:
        logger.warning('No cache found')
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
                     if (event['starts_at'].date() >= today)
                         and event['starts_at'].date() <= timeline_limit),
                    key=itemgetter('starts_at'))

    logger.info('Processing location')
    for event in events:
        event['location'] = fetch_location(event['location_raw'])

    logger.info('Syncing with Discord')
    discord_sync.run(sync_scheduled_events, events)


async def sync_scheduled_events(client, events):
    discord_events = {re.search(r'https?://\S+', e.description).group(0): e
                      for e in client.club_guild.scheduled_events
                      if (int(e.creator_id) == ClubMemberID.BOT
                          and NAME_PREFIX in e.name)}
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
            with mutating_discord(client.club_guild) as proxy:
                await proxy.create_scheduled_event(
                    image=(IMAGES_DIR / event['poster_path']).read_bytes(),
                    **params,
                )
        else:
            logger.info(f"Updating Discord event: {event['name']!r}, {event['url']}")
            with mutating_discord(discord_event) as proxy:
                discord_event = await proxy.edit(
                    cover=(IMAGES_DIR / event['poster_path']).read_bytes(),
                    **params,
                )
    for discord_event in discord_events.values():
        logger.info(f"Canceling Discord event: {discord_event.name!r}, {discord_event.url}")
        with mutating_discord(discord_event) as proxy:
            await proxy.cancel()


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
