from pathlib import Path

import arrow
from playhouse.shortcuts import model_to_dict
from strictyaml import Datetime, Map, Seq, Str, Url, Int, Optional, load

from juniorguru.models import Event, EventSpeaking, db
from juniorguru.lib.images import html_to_png_path#, save_png_as_square
from juniorguru.lib.log import get_log
from juniorguru.lib.template_filters import local_time, md, weekday


log = get_log('events')


DATA_DIR = Path(__file__).parent.parent / 'data'


schema = Seq(
    Map({
        'title': Str(),
        'date': Datetime(),
        Optional('time', default='18:00'): Str(),
        'description': Str(),
        Optional('poster_description'): Str(),
        Optional('bio'): Str(),
        Optional('bio_links'): Seq(Str()),
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
                log.info(f"Marking member {speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event)

            log.info(f"Rendering poster for '{record['title']}'")
            png_path = html_to_png_path('poster.html', model_to_dict(event), DATA_DIR / 'images' / 'posters', filters={
                'md': md,
                'local_time': local_time,
                'weekday': weekday,
            })
            event.poster_path = png_path.relative_to(DATA_DIR)
            event.save()

            # TODO for now commented out to speed up debugging, but works
            # log.info(f"Rendering square poster for '{record['title']}'")
            # save_png_as_square(png_path)




def load_record(record):
    start_at = arrow.get(*map(int, str(record.pop('date').date()).split('-')),
                         *map(int, record.pop('time').split(':')),
                         tzinfo='Europe/Prague')
    record['start_at'] = start_at.to('UTC').naive
    return record


if __name__ == '__main__':
    main()
