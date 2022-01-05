import csv
from datetime import timedelta

import ics
from pod2gen import Podcast, Episode, Media, Person, Category

from juniorguru.lib.md import md
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
    person_h = Person('Honza Javorek', 'honza@junior.guru')
    person_p = Person('Pája Froňková')

    authors = [person_p, person_h]
    copyright = f'© {PodcastEpisode.copyright_year()} Pavlína Froňková, Jan Javorek'

    podcast = Podcast(name='Junior Guru podcast',
                      description='...',
                      language='cs',
                      category=Category('Technology'),  # TODO Category('Business'), Category('Education')
                      website='https://junior.guru/podcast',
                      feed_url='https://junior.guru/api/podcast.xml',
                      authors=authors,
                      owner=person_h,
                      web_master=person_h,
                      copyright=copyright,
                      generator='JuniorGuruBot (+https://junior.guru)',
                      explicit=False)

    for db_episode in PodcastEpisode.api_listing():
        episode = Episode(id=db_episode.global_id,
                          title=db_episode.title_numbered,
                          publication_date=db_episode.publish_at_prg,
                          # link='', TODO
                          summary=md(db_episode.description))
        episode.media = Media(db_episode.media_url,
                              size=db_episode.media_size,
                              type=db_episode.media_type,
                              duration=timedelta(seconds=db_episode.media_duration_s))
        podcast.add_episode(episode)

    podcast.rss_file(str(api_dir / 'podcast.xml'))
