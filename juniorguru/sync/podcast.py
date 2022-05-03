import os
from datetime import date
from multiprocessing import Pool
from pathlib import Path

import requests
from pod2gen import Media
from requests.exceptions import HTTPError
from strictyaml import Datetime, Map, Seq, Str, load, Optional, Int

from juniorguru.lib import loggers
from juniorguru.lib.images import render_image_file, is_image, validate_image
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.podcast import PodcastEpisode
from juniorguru.lib.template_filters import icon


logger = loggers.get(__name__)


YAML_PATH = Path(__file__).parent.parent / 'data' / 'podcast.yml'

YAML_SCHEMA = Seq(
    Map({
        'id': Str(),
        'title': Str(),
        'avatar_path': Str(),
        'publish_on': Datetime(),
        'description': Str(),
        Optional('media_size'): Int(),
        Optional('media_duration_s'): Int(),
    })
)

WORKERS = 2

FLUSH_POSTERS_PODCAST = bool(int(os.getenv('FLUSH_POSTERS_PODCAST', 0)))

IMAGES_DIR = Path(__file__).parent.parent / 'images'

POSTERS_DIR = IMAGES_DIR / 'posters-podcast'

AVATARS_DIR = IMAGES_DIR / 'avatars-participants'

POSTER_WIDTH = 700

POSTER_HEIGHT = 700

TODAY = date.today()


@sync_task()
@db.connection_context()
def main():
    if FLUSH_POSTERS_PODCAST:
        logger.warning("Removing all existing posters for companies, FLUSH_POSTERS_PODCAST is set")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    logger.info('Validating avatar images')
    for path in filter(is_image, AVATARS_DIR.glob('*.*')):
        logger.debug(f'Validating {path}')
        validate_image(path)

    logger.info('Setting up podcast episodes db table')
    PodcastEpisode.drop_table()
    PodcastEpisode.create_table()

    logger.info('Reading YAML with episodes')
    yaml_records = (record.data for record in load(YAML_PATH.read_text(), YAML_SCHEMA))

    logger.info('Preparing data: downloading and analyzing the mp3 files, creating posters')
    records = filter(None, Pool(WORKERS).imap_unordered(process_episode, yaml_records))

    logger.info('Saving to database')
    for record in records:
        PodcastEpisode.create(**record)


def process_episode(yaml_record):
    id = yaml_record['id']
    ep_logger = logger.getChild(id)
    ep_logger.info(f'Processing episode #{id}')

    media_url = f"https://podcast.junior.guru/episodes/{id}.mp3"
    media_type = 'audio/mpeg'
    publish_on = yaml_record['publish_on'].date()

    avatar_path = yaml_record['avatar_path']
    ep_logger.info(f'Checking {avatar_path}')
    image_path = IMAGES_DIR / avatar_path
    if not image_path.exists():
        raise ValueError(f"Episode references '{image_path}', but it doesn't exist")

    ep_logger.info(f'Analyzing {media_url}')
    try:
        if yaml_record.get('media_size') is None or yaml_record.get('media_duration_s') is None:
            ep_logger.warning('Media size and duration not found in YAML, downloading the audio file')
            media = Media.create_from_server_response(media_url, type=media_type)
            media.fetch_duration()
            media_size = media.size
            media_type = media.type
            media_duration_s = media.duration.seconds
            ep_logger.warning(f'Add the following to {YAML_PATH}:\n  media_size: {media_size}\n  media_duration_s: {media_duration_s}')
        else:
            ep_logger.info('Using media size and duration from YAML and only verifying the audio file exists')
            response = requests.head(media_url)
            response.raise_for_status()
            media_size = yaml_record['media_size']
            media_duration_s = yaml_record['media_duration_s']
    except HTTPError as e:
        if publish_on >= TODAY and e.response.status_code == 404:
            ep_logger.warning(f"Future episode {media_url} doesn't exist yet")
            return None
        raise

    data = dict(id=id,
                publish_on=publish_on,
                title=yaml_record['title'],
                avatar_path=avatar_path,
                description=yaml_record['description'],
                media_url=media_url,
                media_size=media_size,
                media_type=media_type,
                media_duration_s=media_duration_s)

    ep_logger.info('Rendering poster')
    episode = PodcastEpisode(**data)
    # The _dirty set causes image cache miss as every time the set gets
    # pickled and serialized to string in different ordering. We won't be
    # saving this object to database, the only purpose is to provide
    # the image renderer with a populated Peewee model object, so let's drop
    # the contents.
    episode._dirty = set()
    tpl_context = dict(episode=episode)
    poster_path = render_image_file(POSTER_WIDTH, POSTER_HEIGHT, 'podcast.html', tpl_context,
                                    POSTERS_DIR, prefix=id, filters=dict(icon=icon))
    data['poster_path'] = poster_path.relative_to(IMAGES_DIR)

    return data
