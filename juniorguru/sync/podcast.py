from multiprocessing import Pool
from pathlib import Path

import arrow
from strictyaml import Map, Seq, Str, Datetime, load
from podgen import Media

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.models import with_db, PodcastEpisode


logger = loggers.get('podcast')


schema = Seq(
    Map({
        'id': Str(),
        'title': Str(),
        'published_at': Datetime(),
        'description': Str(),
    })
)


@measure('podcast')
@with_db
def main():
    PodcastEpisode.drop_table()
    PodcastEpisode.create_table()

    logger.info('Reading YAML with episodes')
    path = Path(__file__).parent.parent / 'data' / 'podcast.yml'
    yaml_records = (record.data for record in load(path.read_text(), schema))

    logger.info('Preparing data by downloading and analyzing the mp3 files')
    records = Pool().map(process_episode, yaml_records)

    logger.info('Saving to database')
    for record in records:
        PodcastEpisode.create(**record)


def process_episode(yaml_record):
    id = yaml_record['id']
    ep_logger = loggers.get(f'podcast.{id}')
    ep_logger.info(f'Processing episode #{id}')

    media_url = f"https://podcast.junior.guru/episodes/{id}.mp3"
    ep_logger.info(f'Analyzing {media_url}')
    media = Media.create_from_server_response(media_url, type='audio/mpeg')
    media.fetch_duration()

    return dict(id=id,
                number=int(id),
                published_at=arrow.get(yaml_record['published_at']).naive,
                title=yaml_record['title'],
                description=yaml_record['description'],
                media_url=media_url,
                media_size=media.size,
                media_type=media.type,
                media_duration_s=media.duration.seconds)


if __name__ == '__main__':
    main()
