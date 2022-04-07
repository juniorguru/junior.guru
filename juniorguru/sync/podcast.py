from datetime import date
from multiprocessing import Pool
from pathlib import Path

from pod2gen import Media
from requests.exceptions import HTTPError
from strictyaml import Datetime, Map, Seq, Str, load

from juniorguru.lib import loggers
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.podcast import PodcastEpisode


logger = loggers.get(__name__)


YAML_SCHEMA = Seq(
    Map({
        'id': Str(),
        'title': Str(),
        'publish_on': Datetime(),
        'description': Str(),
    })
)

WORKERS = 2

TODAY = date.today()


@sync_task()
@db.connection_context()
def main():
    PodcastEpisode.drop_table()
    PodcastEpisode.create_table()

    logger.info('Reading YAML with episodes')
    path = Path(__file__).parent.parent / 'data' / 'podcast.yml'
    yaml_records = (record.data for record in load(path.read_text(), YAML_SCHEMA))

    logger.info('Preparing data by downloading and analyzing the mp3 files')
    records = filter(None, Pool(WORKERS).map(process_episode, yaml_records))

    logger.info('Saving to database')
    for record in records:
        PodcastEpisode.create(**record)


def process_episode(yaml_record):
    id = yaml_record['id']
    ep_logger = logger.getChild(id)
    ep_logger.info(f'Processing episode #{id}')

    media_url = f"https://podcast.junior.guru/episodes/{id}.mp3"
    publish_on = yaml_record['publish_on'].date()

    ep_logger.info(f'Analyzing {media_url}')
    try:
        media = Media.create_from_server_response(media_url, type='audio/mpeg')
        media.fetch_duration()
    except HTTPError as e:
        if publish_on >= TODAY and e.response.status_code == 404:
            ep_logger.warning(f"Future episode {media_url} doesn't exist yet")
            return None
        raise

    return dict(id=id,
                publish_on=publish_on,
                title=yaml_record['title'],
                description=yaml_record['description'],
                media_url=media_url,
                media_size=media.size,
                media_type=media.type,
                media_duration_s=media.duration.seconds)
