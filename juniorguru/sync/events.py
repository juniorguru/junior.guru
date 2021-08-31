import os
from pathlib import Path
from datetime import date, timedelta

import arrow
from strictyaml import Datetime, Map, Seq, Str, Url, Int, Optional, load

from juniorguru.lib.timer import measure
from juniorguru.models import Event, EventSpeaking, ClubMessage, db
from juniorguru.lib.images import render_image_file, downsize_square_photo, save_as_ig_square, replace_with_jpg
from juniorguru.lib.log import get_log
from juniorguru.lib.md import strip_links
from juniorguru.lib.template_filters import local_time, md, weekday
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, discord_task


log = get_log('events')


FLUSH_POSTERS_EVENTS = bool(int(os.getenv('FLUSH_POSTERS_EVENTS', 0)))
DATA_DIR = Path(__file__).parent.parent / 'data'
IMAGES_DIR = Path(__file__).parent.parent / 'images'
POSTERS_DIR = IMAGES_DIR / 'posters-events'

WEB_THUMBNAIL_WIDTH = 1280
WEB_THUMBNAIL_HEIGHT = 672

YOUTUBE_THUMBNAIL_WIDTH = 1160
YOUTUBE_THUMBNAIL_HEIGHT = 735

ANNOUNCEMENTS_CHANNEL = 789046675247333397
EVENTS_CHAT_CHANNEL = 821411678167367691


schema = Seq(
    Map({
        'title': Str(),
        'date': Datetime(),
        Optional('time', default='18:00'): Str(),
        'description': Str(),
        Optional('poster_description'): Str(),
        Optional('avatar_path'): Str(),
        'bio_name': Str(),
        Optional('bio_title'): Str(),
        'bio': Str(),
        Optional('bio_links'): Seq(Str()),
        Optional('logo_path'): Str(),
        'speakers': Seq(Int()),
        Optional('recording_url'): Url(),
    })
)


@measure('events')
def main():
    path = DATA_DIR / 'events.yml'
    records = [load_record(record.data) for record in load(path.read_text(), schema)]

    if FLUSH_POSTERS_EVENTS:
        log.warning("Removing all existing posters for events, FLUSH_POSTERS_EVENTS is set")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    with db:
        db.drop_tables([Event, EventSpeaking])
        db.create_tables([Event, EventSpeaking])

        # process data from the YAML, generate posters
        for record in records:
            name = record['title']
            log.info(f"Creating '{name}'")
            speakers_ids = record.pop('speakers', [])
            event = Event.create(**record)

            for speaker_id in speakers_ids:
                try:
                    avatar_path = next((IMAGES_DIR / 'avatars-speakers').glob(f"{speaker_id}.*"))
                except StopIteration:
                    log.info(f"Didn't find speaker avatar for {speaker_id}")
                    avatar_path = None
                else:
                    log.info(f"Downsizing speaker avatar for {speaker_id}")
                    avatar_path = replace_with_jpg(downsize_square_photo(avatar_path, 500))
                    avatar_path = avatar_path.relative_to(IMAGES_DIR)

                log.info(f"Marking member {speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event,
                                     avatar_path=avatar_path)

            if event.logo_path:
                log.info(f"Checking '{event.logo_path}'")
                image_path = IMAGES_DIR / event.logo_path
                if not image_path.exists():
                    raise ValueError(f"Event '{name}' references '{image_path}', but it doesn't exist")

            log.info(f"Rendering images for '{name}'")
            tpl_context = dict(event=event)
            tpl_filters = dict(md=md, local_time=local_time, weekday=weekday)
            image_path = render_image_file(WEB_THUMBNAIL_WIDTH, WEB_THUMBNAIL_HEIGHT,
                                           'poster.html', tpl_context, POSTERS_DIR,
                                           filters=tpl_filters)
            event.poster_path = image_path.relative_to(IMAGES_DIR)
            image_path = render_image_file(YOUTUBE_THUMBNAIL_WIDTH, YOUTUBE_THUMBNAIL_HEIGHT,
                                           'poster.html', tpl_context, POSTERS_DIR,
                                           filters=tpl_filters, suffix='yt')
            event.poster_yt_path = image_path.relative_to(IMAGES_DIR)
            event.poster_ig_path = save_as_ig_square(image_path).relative_to(IMAGES_DIR)

            log.info(f"Saving '{name}'")
            event.save()

        # discord messages
        if DISCORD_MUTATIONS_ENABLED:
            post_next_event_messages()
        else:
            log.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


@discord_task
async def post_next_event_messages(client):
    announcements_channel = await client.fetch_channel(ANNOUNCEMENTS_CHANNEL)
    events_chat_channel = await client.fetch_channel(EVENTS_CHAT_CHANNEL)

    event = Event.next()
    if not event:
        log.info("The next event is not announced yet")
        return
    speakers = ', '.join([speaking.speaker.mention for speaking in event.list_speaking])

    log.info("About to post a message 7 days prior to the event")
    if event.start_at.date() - timedelta(days=7) <= date.today():
        with db:
            message = ClubMessage.last_bot_message(ANNOUNCEMENTS_CHANNEL, '🗓', event.url)
        if message:
            log.info(f'Looks like the message already exists: {message.url}')
        else:
            log.info("Found no message, posting!")
            content = f"🗓 Už **za týden** bude v klubu „{event.title}” s {speakers}! {event.url}"
            await announcements_channel.send(content)
    else:
        log.info("It's not 7 days prior to the event")

    log.info("About to post a message 1 day prior to the event")
    if event.start_at.date() - timedelta(days=1) == date.today():
        with db:
            message = ClubMessage.last_bot_message(ANNOUNCEMENTS_CHANNEL, '🤩', event.url)
        if message:
            log.info(f'Looks like the message already exists: {message.url}')
        else:
            log.info("Found no message, posting!")
            content = f"🤩 Už **zítra v {event.start_at_prg:%H:%M}** bude v klubu „{event.title}” s {speakers}! {event.url}"
            await announcements_channel.send(content)
    else:
        log.info("It's not 1 day prior to the event")

    log.info("About to post a message on the day when the event is")
    if event.start_at.date() == date.today():
        with db:
            message = ClubMessage.last_bot_message(ANNOUNCEMENTS_CHANNEL, '⏰', event.url)
        if message:
            log.info(f'Looks like the message already exists: {message.url}')
        else:
            log.info("Found no message, posting!")
            content = f"⏰ @everyone Už **dnes v {event.start_at_prg:%H:%M}** bude v klubu „{event.title}” s {speakers}! Odehrávat se to bude v klubovně, případné dotazy v {events_chat_channel.mention} 💬 Akce se nahrávají, odkaz na záznam se objeví v tomto kanálu. {event.url}"
            await announcements_channel.send(content)
    else:
        log.info("It's not the day when the event is")

    log.info("About to post a message to event chat on the day when the event is")
    if event.start_at.date() == date.today():
        with db:
            message = ClubMessage.last_bot_message(EVENTS_CHAT_CHANNEL, '👋', event.url)
        if message:
            log.info(f'Looks like the message already exists: {message.url}')
        else:
            log.info("Found no message, posting!")
            content = [
                f"👋 Už **dnes v {event.start_at_prg:%H:%M}** tady bude probíhat „{event.title}” s {speakers} (viz {announcements_channel.mention}). Tento kanál slouží k pokládání dotazů, sdílení odkazů, slajdů k prezentaci…",
                "",
                "⚠️ Ve výchozím nastavení Discord udělá zvuk při každé aktivitě v hlasovém kanálu, např. při připojení nového účastníka, odpojení, vypnutí zvuku, zapnutí, apod. Zvuky si vypni v _User Settings_, stránka _Notifications_, sekce _Sounds_. Většina zvuků souvisí s hovory, takže je potřeba povypínat skoro vše.",
                "",
                f"ℹ️ {strip_links(event.description.strip())}",
                "",
                f"🦸 {strip_links(event.bio).strip()}"
                "",
                "",
                f"👉 {event.url}",
            ]
            await events_chat_channel.send('\n'.join(content))
    else:
        log.info("It's not the day when the event is")


def load_record(record):
    start_at = arrow.get(*map(int, str(record.pop('date').date()).split('-')),
                         *map(int, record.pop('time').split(':')),
                         tzinfo='Europe/Prague')
    record['start_at'] = start_at.to('UTC').naive
    return record


if __name__ == '__main__':
    main()
