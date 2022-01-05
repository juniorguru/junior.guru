import csv
from datetime import timedelta

import ics
from podgen import Podcast, Episode, Media

from juniorguru.models import Employment, Event, PodcastEpisode, with_db


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


@with_db
def build_podcast_xml(api_dir, config):
    podcast = Podcast(name='Junior Guru podcast',
                      description='...',
                      website='https://junior.guru',
                      explicit=False)
    for db_episode in PodcastEpisode.api_listing():
        episode = Episode(id=db_episode.id,
                          title=db_episode.title_numbered,
                          publication_date=db_episode.published_at_prg,
                          subtitle='...',
                          summary='...',
                          long_summary='...')
        episode.media = Media(db_episode.media_url,
                              size=db_episode.media_size,
                              type=db_episode.media_type,
                              duration=timedelta(seconds=db_episode.media_duration_s))
        podcast.add_episode(episode)
    podcast.rss_file(str(api_dir / 'podcast.xml'))
