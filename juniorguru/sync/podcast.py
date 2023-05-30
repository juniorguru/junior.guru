from datetime import date
from multiprocessing import Pool
from pathlib import Path

import click
import requests
from discord import Color, Embed, File, ui
from pod2gen import Media
from requests.exceptions import HTTPError
from strictyaml import Int, Map, Optional, Seq, Str, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import ClubChannelID, ClubMemberID
from juniorguru.lib.images import is_image, render_image_file, validate_image
from juniorguru.lib.mutations import mutating_discord
from juniorguru.lib.template_filters import icon
from juniorguru.lib.yaml import Date
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.partner import Partner
from juniorguru.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


YAML_PATH = Path('juniorguru/data/podcast.yml')

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

WORKERS = 4

IMAGES_DIR = Path('juniorguru/images')

POSTERS_DIR = IMAGES_DIR / 'posters-podcast'

AVATARS_DIR = IMAGES_DIR / 'avatars-participants'

POSTER_WIDTH = 700

POSTER_HEIGHT = 700

TODAY = date.today()

MESSAGE_EMOJI = '🎙'


@cli.sync_command(dependencies=['club-content', 'partners'])
@click.option('--flush-posters/--no-flush-posters', default=False)
@db.connection_context()
def main(flush_posters):
    if flush_posters:
        logger.warning("Removing all existing posters for podcast episodes")
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

    logger.info('Announcing in Discord')
    discord_sync.run(discord_task)


def process_episode(yaml_record):
    id = yaml_record['id']
    logger_ep = logger[id]
    logger_ep.info(f'Processing episode #{id}')

    media_url = f"https://podcast.junior.guru/episodes/{id}.mp3"
    media_type = 'audio/mpeg'

    avatar_path = yaml_record['avatar_path']
    logger_ep.debug(f'Checking {avatar_path}')
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

    logger_ep.debug('Figuring out partner')
    if 'partner' in yaml_record:
        with db.connection_context():
            partner = Partner.get_by_slug(yaml_record['partner'])
        logger_ep.info(f'Partner: {partner.name}')
    else:
        partner = None

    logger_ep.debug('Preparing data')
    data = dict(id=id,
                publish_on=yaml_record['publish_on'],
                title=yaml_record['title'],
                avatar_path=avatar_path,
                description=yaml_record['description'],
                media_url=media_url,
                media_size=media_size,
                media_type=media_type,
                media_duration_s=media_duration_s,
                partner=partner)

    logger_ep.debug('Rendering poster')
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
    last_message = ClubMessage.last_bot_message(ClubChannelID.ANNOUNCEMENTS, MESSAGE_EMOJI, f'**{last_episode.number}. epizodu**')
    if not last_message:
        logger.info(f'Announcing {last_episode!r}')
        channel = await client.fetch_channel(ClubChannelID.ANNOUNCEMENTS)
        content = (
            f"{MESSAGE_EMOJI} Nastraž uši! <@{ClubMemberID.PAVLINA}>"
            f" natočila **{last_episode.number}. epizodu** podcastu!"
        )

        description_embed = Embed(title=last_episode.title_numbered,
                                    description=last_episode.description.strip(),
                                    color=Color.yellow())
        description_embed.set_thumbnail(url=f"attachment://{Path(last_episode.poster_path).name}")
        poster_file = File(IMAGES_DIR / last_episode.poster_path)

        if last_episode.partner:
            details = (
                ':star: Epizoda vznikla v rámci'
                f' [placeného partnerství](https://junior.guru/open/{last_episode.partner.slug})'
                f' s firmou [{last_episode.partner.name}]({last_episode.partner.url}'
                '?utm_source=juniorguru&utm_medium=podcast&utm_campaign=partnership)'
                '\n'
            )
        else:
            details = ''
        details += (
            f"⏱️ {last_episode.media_duration_m} minut poslechu\n"
            f"<a:vincent:900831887591882782> Do půl hodiny to bude na webu, brzo potom i na ostatních službách\n"
        )
        details_embed = Embed(description=details)

        view = ui.View(ui.Button(emoji='<:juniorguru:841683119291760640>',
                                    label='web',
                                    url='https://junior.guru/podcast/'),
                        ui.Button(emoji='<:youtube:976200175490060299>',
                                    label='YouTube',
                                    url='https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA'),
                        ui.Button(emoji='<:spotify:1085596335794819092>',
                                    label='Spotify',
                                    url='https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4'),
                        ui.Button(emoji='<:google:976200950886826084>',
                                    label='Google',
                                    url='https://podcasts.google.com/feed/aHR0cHM6Ly9qdW5pb3IuZ3VydS9hcGkvcG9kY2FzdC54bWw'),
                        ui.Button(emoji='<:appleinc:842465215718227987>',
                                    label='Apple',
                                    url='https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549'))
        with mutating_discord(channel) as proxy:
            await proxy.send(content=content,
                               embeds=[description_embed, details_embed],
                               files=[poster_file],
                               view=view)
    else:
        logger.info(f'Looks like {last_episode!r} has been already announced')
