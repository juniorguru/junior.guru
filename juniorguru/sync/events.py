from datetime import date, timedelta
from pathlib import Path

import arrow
import click
from strictyaml import CommaSeparated, Int, Map, Optional, Seq, Str, Url, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import ClubChannel, mutating
from juniorguru.lib.images import is_image, render_image_file, validate_image
from juniorguru.lib.mutations import MutationsNotAllowedError
from juniorguru.lib.template_filters import local_time, md, weekday
from juniorguru.lib.yaml import Date
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.event import Event, EventSpeaking
from juniorguru.models.partner import Partner


logger = loggers.from_path(__file__)


DATA_PATH = Path(__file__).parent.parent / 'data' / 'events.yml'

IMAGES_DIR = Path(__file__).parent.parent / 'images'

POSTERS_DIR = IMAGES_DIR / 'posters-events'

AVATARS_DIR = IMAGES_DIR / 'avatars-participants'

YOUTUBE_THUMBNAIL_WIDTH = 1280

YOUTUBE_THUMBNAIL_HEIGHT = 720

DISCORD_THUMBNAIL_WIDTH = 1280

DISCORD_THUMBNAIL_HEIGHT = 512


schema = Seq(
    Map({
        'title': Str(),
        'date': Date(),
        Optional('time', default='18:00'): Str(),
        'description': Str(),
        Optional('poster_description'): Str(),
        Optional('avatar_path'): Str(),
        'bio_name': Str(),
        Optional('bio_title'): Str(),
        'bio': Str(),
        Optional('bio_links'): Seq(Str()),
        Optional('partner'): Str(),
        Optional('logo_path'): Str(),
        'speakers': CommaSeparated(Int()),
        Optional('recording_url'): Url(),
        Optional('public_recording_url'): Url(),
    })
)


@cli.sync_command(dependencies=['club-content', 'partners'])
@click.option('--flush-posters/--no-flush-posters', default=False)
def main(flush_posters):
    if flush_posters:
        logger.warning("Removing all existing posters for events")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    logger.info('Validating avatar images')
    for path in filter(is_image, AVATARS_DIR.glob('*.*')):
        logger.debug(f'Validating {path}')
        validate_image(path)

    with db.connection_context():
        logger.info('Setting up events db tables')
        db.drop_tables([Event, EventSpeaking])
        db.create_tables([Event, EventSpeaking])

        logger.info('Processing data from the YAML, creating posters')
        records = [load_record(record.data) for record in load(DATA_PATH.read_text(), schema)]
        for record in records:
            name = record['title']
            logger.info(f"Creating '{name}'")
            speakers_ids = record.pop('speakers', [])
            if 'partner' in record:
                record['partner'] = Partner.get_by_slug(record['partner'])
            event = Event.create(**record)

            for speaker_id in speakers_ids:
                logger.info(f"Marking member #{speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event)

            logger.debug(f"Checking '{event.avatar_path}'")
            image_path = IMAGES_DIR / event.avatar_path
            if not image_path.exists():
                raise ValueError(f"Event '{name}' references '{image_path}', but it doesn't exist")

            if event.logo_path:
                logger.debug(f"Checking '{event.logo_path}'")
                image_path = IMAGES_DIR / event.logo_path
                if not image_path.exists():
                    raise ValueError(f"Event '{name}' references '{image_path}', but it doesn't exist")

            logger.info(f"Rendering posters for '{name}'")
            tpl_context = dict(event=event)
            tpl_filters = dict(md=md, local_time=local_time, weekday=weekday)
            prefix = event.start_at.date().isoformat().replace('-', '')
            image_path = render_image_file(DISCORD_THUMBNAIL_WIDTH, DISCORD_THUMBNAIL_HEIGHT,
                                            'event.html', tpl_context, POSTERS_DIR,
                                            filters=tpl_filters, prefix=prefix, suffix='dc')
            event.poster_dc_path = image_path.relative_to(IMAGES_DIR)
            image_path = render_image_file(YOUTUBE_THUMBNAIL_WIDTH, YOUTUBE_THUMBNAIL_HEIGHT,
                                            'event.html', tpl_context, POSTERS_DIR,
                                            filters=tpl_filters, prefix=prefix, suffix='yt')
            event.poster_yt_path = image_path.relative_to(IMAGES_DIR)
            logger.info(f"Saving '{name}'")
            event.save()

    logger.info('Syncing with Discord')
    discord_sync.run(sync_scheduled_events)
    discord_sync.run(post_next_event_messages)


@db.connection_context()
async def sync_scheduled_events(client):
    discord_events = {arrow.get(e.start_time).naive: e
                      for e in client.club_guild.scheduled_events}
    channel = await client.fetch_channel(ClubChannel.EVENTS)
    for event in Event.planned_listing():
        discord_event = discord_events.get(event.start_at)
        if discord_event:
            logger.info(f"Discord event for '{event.title}' already exists, updating")
            with mutating(discord_event) as proxy:
                discord_event = await proxy.edit(
                    name=f'{event.bio_name}: {event.title}',
                    description=f'{event.description_plain}\n\n{event.bio_plain}\n\n{event.url}',
                    end_time=event.end_at,
                    cover=(IMAGES_DIR / event.poster_dc_path).read_bytes(),
                )
        else:
            logger.info(f"Creating Discord event for '{event.title}'")
            try:
                with mutating(client.club_guild, raises=True) as proxy:
                    discord_event = await proxy.create_scheduled_event(
                        name=f'{event.bio_name}: {event.title}',
                        description=f'{event.description_plain}\n\n{event.bio_plain}\n\n{event.url}',
                        start_time=event.start_at,
                        end_time=event.end_at,
                        location=channel,
                    )
            except MutationsNotAllowedError:
                pass
            else:
                event.discord_id = discord_event.id
                event.discord_url = discord_event.url
                event.save()


@db.connection_context()
async def post_next_event_messages(client):
    announcements_channel = await client.fetch_channel(ClubChannel.ANNOUNCEMENTS)
    events_channel = await client.fetch_channel(ClubChannel.EVENTS)

    event = Event.next()
    if not event:
        logger.info("The next event is not announced yet")
        return
    speakers = ', '.join([speaking.speaker.mention for speaking in event.list_speaking])
    speakers = speakers or event.bio_name

    logger.info("About to post a message 7 days prior to the event")
    if event.start_at.date() - timedelta(days=7) <= date.today():
        message = ClubMessage.last_bot_message(ClubChannel.ANNOUNCEMENTS, '🗓', event.discord_url)
        if message:
            logger.info(f'Looks like the message already exists: {message.url}')
        else:
            logger.info("Found no message, posting!")
            content = f"🗓 Už **za týden** bude v klubu akce „{event.title}” s {speakers}! {event.discord_url}"
            with mutating(announcements_channel) as proxy:
                await proxy.send(content)
    else:
        logger.info("It's not 7 days prior to the event")

    logger.info("About to post a message 1 day prior to the event")
    if event.start_at.date() - timedelta(days=1) == date.today():
        message = ClubMessage.last_bot_message(ClubChannel.ANNOUNCEMENTS, '🤩', event.discord_url)
        if message:
            logger.info(f'Looks like the message already exists: {message.url}')
        else:
            logger.info("Found no message, posting!")
            content = f"🤩 Už **zítra v {event.start_at_prg:%H:%M}** bude v klubu akce „{event.title}” s {speakers}! {event.discord_url}"
            with mutating(announcements_channel) as proxy:
                await proxy.send(content)
    else:
        logger.info("It's not 1 day prior to the event")

    logger.info("About to post a message on the day when the event is")
    if event.start_at.date() == date.today():
        message = ClubMessage.last_bot_message(ClubChannel.ANNOUNCEMENTS, '⏰', event.discord_url)
        if message:
            logger.info(f'Looks like the message already exists: {message.url}')
        else:
            logger.info("Found no message, posting!")
            content = f"⏰ @everyone Už **dnes v {event.start_at_prg:%H:%M}** bude v klubu akce „{event.title}” s {speakers}! Odehrávat se to bude v {events_channel.mention}, dotazy jde pokládat v tamním chatu 💬 Akce se nahrávají, odkaz na záznam se objeví v tomto kanálu. {event.discord_url}"
            with mutating(announcements_channel) as proxy:
                await proxy.send(content)
    else:
        logger.info("It's not the day when the event is")

    # See https://github.com/Pycord-Development/pycord/issues/1934
    #
    # logger.info("About to post a message to event chat on the day when the event is")
    # if event.start_at.date() == date.today():
    #     message = ClubMessage.last_bot_message(ClubChannel.EVENTS, '👋', event.discord_url)
    #     if message:
    #         logger.info(f'Looks like the message already exists: {message.url}')
    #     else:
    #         logger.info("Found no message, posting!")
    #         content = [
    #             f"👋 Už **dnes v {event.start_at_prg:%H:%M}** tady bude probíhat „{event.title}” s {speakers} (viz {announcements_channel.mention}). Tento kanál slouží k pokládání dotazů, sdílení odkazů, slajdů k prezentaci…",
    #             "",
    #             "⚠️ Ve výchozím nastavení Discord udělá zvuk při každé aktivitě v hlasovém kanálu, např. při připojení nového účastníka, odpojení, vypnutí zvuku, zapnutí, apod. Zvuky si vypni v Uživatelských nastaveních (_User Settings_), na stránce Oznámení (_Notifications_), sekce Zvuky (_Sounds_). Většina zvuků souvisí s hovory, takže je potřeba povypínat skoro vše.",
    #             "",
    #             f"📺 Limit přímých účastníků je 25, takže přijďte včas. Kdo se nevleze, bude mít možnost sledovat stream na YouTube, odkaz se kdyžtak objeví tady v chatu. Záznam se po akci objeví v {announcements_channel.mention}.",
    #             "",
    #             f"ℹ️ {event.description_plain}",
    #             "",
    #             f"🦸 {event.bio_plain}"
    #             "",
    #             "",
    #             f"👉 {event.url}",
    #         ]
    #         with mutating(events_channel) as proxy:
    #             await proxy.send('\n'.join(content))
    # else:
    #     logger.info("It's not the day when the event is")


def load_record(record):
    start_at = arrow.get(*map(int, str(record.pop('date')).split('-')),
                         *map(int, record.pop('time').split(':')),
                         tzinfo='Europe/Prague')
    record['start_at'] = start_at.to('UTC').naive
    return record
