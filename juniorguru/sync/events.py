import os
from pathlib import Path

import arrow
from playhouse.shortcuts import model_to_dict
from strictyaml import Datetime, Map, Seq, Str, Url, Int, Optional, load

from juniorguru.models import Event, EventSpeaking, db
from juniorguru.lib.images import render_image_file, downsize_square_photo, save_as_ig_square
from juniorguru.lib.log import get_log
from juniorguru.lib.template_filters import local_time, md, weekday


log = get_log('events')


FLUSH_POSTERS = bool(int(os.getenv('FLUSH_POSTERS', 0)))
DATA_DIR = Path(__file__).parent.parent / 'data'
IMAGES_DIR = Path(__file__).parent.parent / 'images'
POSTERS_DIR = IMAGES_DIR / 'posters'


schema = Seq(
    Map({
        'title': Str(),
        'date': Datetime(),
        Optional('time', default='18:00'): Str(),
        'description': Str(),
        Optional('poster_description'): Str(),
        Optional('bio'): Str(),
        Optional('bio_title'): Str(),
        Optional('bio_links'): Seq(Str()),
        Optional('logo_path'): Str(),
        'speakers': Seq(Int()),
        Optional('recording_url'): Url(),
    })
)


def main():
    path = DATA_DIR / 'events.yml'
    records = [load_record(record.data) for record in load(path.read_text(), schema)]

    if FLUSH_POSTERS:
        log.warning("Removing all existing posters, FLUSH_POSTERS is set")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    with db:
        db.drop_tables([Event, EventSpeaking])
        db.create_tables([Event, EventSpeaking])

        for record in records:
            name = record['title']
            log.info(f"Creating '{name}'")
            speakers_ids = record.pop('speakers', [])
            event = Event.create(**record)

            for speaker_id in speakers_ids:
                try:
                    avatar_path = next((IMAGES_DIR / 'speakers').glob(f"{speaker_id}.*"))
                except StopIteration:
                    log.info(f"Didn't find speaker avatar for {speaker_id}")
                    avatar_path = None
                else:
                    log.info(f"Downsizing speaker avatar for {speaker_id}")
                    avatar_path = downsize_square_photo(avatar_path, 500).relative_to(IMAGES_DIR)

                log.info(f"Marking member {speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event,
                                     avatar_path=avatar_path)

            if event.logo_path:
                log.info(f"Checking '{event.logo_path}'")
                image_path = IMAGES_DIR / event.logo_path
                if not image_path.exists():
                    raise ValueError(f"Event '{name}' references '{image_path}', but it doesn't exist")

            log.info(f"Rendering poster for '{name}'")
            context = dict(event=model_to_dict(event, extra_attrs=['first_avatar_path']))
            image_path = render_image_file('poster.html', context, POSTERS_DIR, filters={
                'md': md,
                'local_time': local_time,
                'weekday': weekday,
            })
            event.poster_path = image_path.relative_to(IMAGES_DIR)
            event.save()

            log.info(f"Rendering Instagram poster for '{name}'")
            save_as_ig_square(image_path)




def load_record(record):
    start_at = arrow.get(*map(int, str(record.pop('date').date()).split('-')),
                         *map(int, record.pop('time').split(':')),
                         tzinfo='Europe/Prague')
    record['start_at'] = start_at.to('UTC').naive
    return record


if __name__ == '__main__':
    main()
