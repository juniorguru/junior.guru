import csv
from datetime import timedelta

import ics

from juniorguru.models import Employment, Event, with_db


@with_db
def build_events_ics(api_dir, config):
    calendar = ics.Calendar(events=[
        ics.Event(summary=event.title,
                  begin=event.start_at,
                  duration=timedelta(hours=1),
                  description=event.url)
        for event in Event.api_listing()
    ])
    api_file = api_dir / 'events.ics'
    with api_file.open('w', encoding='utf-8') as f:
        f.writelines(calendar)


@with_db
def build_czechitas_csv(api_dir, config):
    rows = [employment.to_api() for employment in Employment.api_listing()]
    api_file = api_dir / 'jobs.csv'
    with api_file.open('w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
