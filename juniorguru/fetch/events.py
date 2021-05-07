from pathlib import Path

import arrow
from strictyaml import Datetime, Map, Seq, Str, Url, Int, Optional, load

from juniorguru.models import Event, EventSpeaking, db


schema = Seq(
    Map({
        'title': Str(),
        'date': Datetime(),
        Optional('time', default='18:00'): Str(),
        'description': Str(),
        Optional('bio'): Str(),
        Optional('bio_links'): Seq(Str()),
        'speakers': Seq(Int()),
        Optional('recording_url'): Url(),
    })
)


def main():
    path = Path(__file__).parent.parent / 'data' / 'events.yml'
    records = [load_record(record.data) for record
               in load(path.read_text(), schema)]

    with db:
        db.drop_tables([Event, EventSpeaking])
        db.create_tables([Event, EventSpeaking])

        for record in records:
            speakers_ids = record.pop('speakers', [])
            event = Event.create(**record)
            for speaker_id in speakers_ids:
                EventSpeaking.create(speaker=speaker_id, event=event)


def load_record(record):
    start_at = arrow.get(*map(int, str(record.pop('date').date()).split('-')),
                         *map(int, record.pop('time').split(':')),
                         tzinfo='Europe/Prague')
    record['start_at'] = start_at.to('UTC').datetime
    return record


if __name__ == '__main__':
    main()
