from pathlib import Path

import arrow
from playhouse.shortcuts import model_to_dict
from strictyaml import Datetime, Map, Seq, Str, Url, Int, Optional, load

from juniorguru.models import Event, EventSpeaking, db
from juniorguru.lib.images import render_image_file, downsize_square_photo#, save_as_ig_square
from juniorguru.lib.log import get_log
from juniorguru.lib.template_filters import local_time, md, weekday


log = get_log('events')


DATA_DIR = Path(__file__).parent.parent / 'data'
IMAGES_DIR = Path(__file__).parent.parent / 'images'


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
        Optional('org_logo'): Str(),
        'speakers': Seq(Int()),
        Optional('recording_url'): Url(),
    })
)


def main():
    path = DATA_DIR / 'events.yml'
    records = [load_record(record.data) for record
               in load(path.read_text(), schema)]

    with db:
        db.drop_tables([Event, EventSpeaking])
        db.create_tables([Event, EventSpeaking])

        for record in records:
            log.info(f"Creating '{record['title']}'")
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
                    avatar_path = downsize_square_photo(avatar_path, 500)

                log.info(f"Marking member {speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event, avatar_path=avatar_path)

            log.info(f"Rendering poster for '{record['title']}'")
            image_path = render_image_file('poster.html', model_to_dict(event), IMAGES_DIR / 'posters', filters={
                'md': md,
                'local_time': local_time,
                'weekday': weekday,
            })
            event.poster_path = image_path.relative_to(IMAGES_DIR)
            event.save()

            # TODO for now commented out to speed up debugging, but works
            # log.info(f"Rendering Instagram poster for '{record['title']}'")
            # save_as_ig_square(image_path)




def load_record(record):
    start_at = arrow.get(*map(int, str(record.pop('date').date()).split('-')),
                         *map(int, record.pop('time').split(':')),
                         tzinfo='Europe/Prague')
    record['start_at'] = start_at.to('UTC').naive
    return record


if __name__ == '__main__':
    main()
