import os
from datetime import date
from multiprocessing import Pool
from pathlib import Path

import requests
from discord import Embed, File
from pod2gen import Media
from requests.exceptions import HTTPError
from strictyaml import Int, Map, Optional, Seq, Str, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import (ANNOUNCEMENTS_CHANNEL, DISCORD_MUTATIONS_ENABLED,
                                 run_discord_task)
from juniorguru.lib.images import is_image, render_image_file, validate_image
from juniorguru.lib.template_filters import icon
from juniorguru.lib.yaml import Date
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.partner import Company
from juniorguru.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


YAML_PATH = Path(__file__).parent.parent / 'data' / 'podcast.yml'

YAML_SCHEMA = Seq(
    Map({
        'id': Str(),
        'title': Str(),
        'avatar_path': Str(),
        'publish_on': Date(),
        'description': Str(),
        Optional('media_size'): Int(),
        Optional('media_duration_s'): Int(),
        Optional('partner'): Str(),
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

MESSAGE_EMOJI = '🎙'


@cli.sync_command(dependencies=['club-content', 'companies'])
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
        if 'partner' in record:
            record['partner'] = Company.get_by_slug(record['partner'])
        PodcastEpisode.create(**record)

    logger.info('Announcing in Discord')
    run_discord_task('juniorguru.sync.podcast.discord_task')


def process_episode(yaml_record):
    id = yaml_record['id']
    logger_ep = logger[id]
    logger_ep.info(f'Processing episode #{id}')

    media_url = f"https://podcast.junior.guru/episodes/{id}.mp3"
    media_type = 'audio/mpeg'

    avatar_path = yaml_record['avatar_path']
    logger_ep.info(f'Checking {avatar_path}')
    image_path = IMAGES_DIR / avatar_path
    if not image_path.exists():
        raise ValueError(f"Episode references '{image_path}', but it doesn't exist")

    logger_ep.info(f'Analyzing {media_url}')
    try:
        if yaml_record.get('media_size') is None or yaml_record.get('media_duration_s') is None:
            logger_ep.warning('Media size and duration not found in YAML, downloading the audio file')
            media = Media.create_from_server_response(media_url, type=media_type)
            media.fetch_duration()
            media_size = media.size
            media_type = media.type
            media_duration_s = media.duration.seconds
            logger_ep.warning(f'Add the following to {YAML_PATH}:\n  media_size: {media_size}\n  media_duration_s: {media_duration_s}')
        else:
            logger_ep.info('Using media size and duration from YAML and only verifying the audio file exists')
            response = requests.head(media_url)
            response.raise_for_status()
            media_size = yaml_record['media_size']
            media_duration_s = yaml_record['media_duration_s']
    except HTTPError as e:
        if yaml_record['publish_on'] >= TODAY and e.response.status_code == 404:
            logger_ep.warning(f"Future episode {media_url} doesn't exist yet")
            return None
        raise

    data = dict(id=id,
                publish_on=yaml_record['publish_on'],
                title=yaml_record['title'],
                avatar_path=avatar_path,
                description=yaml_record['description'],
                media_url=media_url,
                media_size=media_size,
                media_type=media_type,
                media_duration_s=media_duration_s)

    logger_ep.info('Rendering poster')
    episode = PodcastEpisode(**data)
    # The _dirty set causes image cache miss as every time the set gets
    # pickled and serialized to string in different ordering. We won't be
    # saving this object to database, the only purpose is to provide
    # the image renderer with a populated Peewee model object, so let's drop
    # the contents.
    episode.clear_dirty_fields()
    tpl_context = dict(episode=episode)
    poster_path = render_image_file(POSTER_WIDTH, POSTER_HEIGHT, 'podcast.html', tpl_context,
                                    POSTERS_DIR, prefix=id, filters=dict(icon=icon))
    data['poster_path'] = poster_path.relative_to(IMAGES_DIR)

    return data


@db.connection_context()
async def discord_task(client):
    last_episode = PodcastEpisode.last()
    last_message = ClubMessage.last_bot_message(ANNOUNCEMENTS_CHANNEL, MESSAGE_EMOJI, f'**{last_episode.number}. díl**')
    if not last_message:
        logger.info(f'Announcing {last_episode!r}')
        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(ANNOUNCEMENTS_CHANNEL)
            content = (
                f"{MESSAGE_EMOJI} Nastraž uši! <@810862212297130005> natočila **{last_episode.number}. díl** junior.guru podcastu!"
            )
            embed_description_lines = [
                f'ℹ️ {last_episode.description.strip()}\n',
                f"🔊 Do půl hodiny se to objeví [na webu]({last_episode.url})",
                "📥 Někdy brzo se to objeví i na všech běžných podcastových službách",
                f"⏳ Díl má {last_episode.media_duration_m} minut",
            ]
            embed = Embed(title=last_episode.title_numbered, description='\n'.join(embed_description_lines))
            embed.set_thumbnail(url=f"attachment://{Path(last_episode.poster_path).name}")
            file = File(IMAGES_DIR / last_episode.poster_path)

            await channel.send(content=content, embed=embed, file=file)
        else:
            logger.warning('Discord mutations not enabled')
    else:
        logger.info(f'Looks like {last_episode!r} has been already announced')
