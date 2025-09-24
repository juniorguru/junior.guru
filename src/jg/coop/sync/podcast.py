from datetime import date, timedelta
from multiprocessing import Pool
from pathlib import Path

import click
import requests
from discord import Color, Embed, File, ui
from pod2gen import Media
from requests.exceptions import HTTPError
from strictyaml import Int, Map, Optional, Seq, Str, load

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubChannelID, ClubClient, ClubMemberID
from jg.coop.lib.images import PostersCache, is_image, render_image_file, validate_image
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.template_filters import icon
from jg.coop.lib.yaml import Date
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.feminine_name import FeminineName
from jg.coop.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


YAML_PATH = Path("src/jg/coop/data/podcast.yml")

YAML_SCHEMA = Seq(
    Map(
        {
            "number": Int(),
            "title": Str(),
            Optional("guest_name"): Str(),
            Optional("guest_affiliation"): Str(),
            "publish_on": Date(),
            "description": Str(),
            "image_path": Str(),
            Optional("media_size"): Int(),
            Optional("media_duration_s"): Int(),
        }
    )
)

WORKERS = 4

IMAGES_DIR = Path("src/jg/coop/images")

POSTERS_DIR = IMAGES_DIR / "posters-podcast"

AVATARS_DIR = IMAGES_DIR / "avatars-participants"

POSTER_WIDTH = 700

POSTER_HEIGHT = 700

TODAY = date.today()

MESSAGE_EMOJI = "🎙"


@cli.sync_command(dependencies=["club-content", "feminine-names"])
@click.option("--clear-posters/--keep-posters", default=False)
@db.connection_context()
def main(clear_posters):
    posters = PostersCache(POSTERS_DIR)
    posters.init(clear=clear_posters)

    logger.info("Validating avatar images")
    for path in filter(is_image, AVATARS_DIR.glob("*.*")):
        logger.debug(f"Validating {path}")
        validate_image(path)

    logger.info("Setting up podcast episodes db table")
    PodcastEpisode.drop_table()
    PodcastEpisode.create_table()

    logger.info("Reading YAML with episodes")
    yaml_records = (record.data for record in load(YAML_PATH.read_text(), YAML_SCHEMA))

    logger.info(
        "Preparing data: downloading and analyzing the mp3 files, creating posters"
    )
    records = filter(None, Pool(WORKERS).imap_unordered(process_episode, yaml_records))

    for record in records:
        logger.info(f"Saving episode #{record['number']}")
        PodcastEpisode.create(**record)
        posters.record(IMAGES_DIR / record["poster_path"])
    posters.cleanup()

    logger.info("Announcing in Discord")
    discord_task.run(announce_new_episode)


def process_episode(yaml_record):
    number = yaml_record["number"]
    logger_ep = logger[number]
    logger_ep.info(f"Processing episode #{number}")

    media_slug = f"{number:04d}"
    media_url = f"https://podcast.junior.guru/episodes/{media_slug}.mp3"
    media_type = "audio/mpeg"

    image_path = yaml_record["image_path"]
    logger_ep.debug(f"Checking {image_path}")
    full_image_path = IMAGES_DIR / image_path
    if not full_image_path.exists():
        raise ValueError(
            f"Episode references {image_path} ({full_image_path}), but it doesn't exist"
        )

    logger_ep.info(f"Analyzing {media_url}")
    try:
        if (
            yaml_record.get("media_size") is None
            or yaml_record.get("media_duration_s") is None
        ):
            logger_ep.warning(
                "Media size and duration not found in YAML, downloading the audio file"
            )
            media = Media.create_from_server_response(media_url, type=media_type)
            media.fetch_duration()
            media_size = media.size
            media_type = media.type
            media_duration_s = media.duration.seconds
            logger_ep.warning(
                f"Add the following to {YAML_PATH}:\n  media_size: {media_size}\n  media_duration_s: {media_duration_s}"
            )
        else:
            logger_ep.info(
                "Using media size and duration from YAML and only verifying the audio file exists"
            )
            response = requests.head(media_url)
            response.raise_for_status()
            media_size = yaml_record["media_size"]
            media_duration_s = yaml_record["media_duration_s"]
    except HTTPError as e:
        if yaml_record["publish_on"] >= TODAY and e.response.status_code == 404:
            logger_ep.warning(f"Future episode {media_url} doesn't exist yet")
            return None
        raise

    if guest_name := yaml_record.get("guest_name"):
        guest_has_feminine_name = FeminineName.is_feminine(guest_name)
    else:
        guest_has_feminine_name = None

    guest_affiliation = yaml_record.get("guest_affiliation")
    if guest_affiliation and not guest_name:
        raise ValueError(f"Episode #{number} is missing guest_name")

    logger_ep.debug("Preparing data")
    data = dict(
        number=number,
        publish_on=yaml_record["publish_on"],
        title=yaml_record["title"],
        guest_name=guest_name,
        guest_has_feminine_name=guest_has_feminine_name,
        guest_affiliation=guest_affiliation,
        image_path=image_path,
        description=yaml_record["description"],
        media_slug=media_slug,
        media_url=media_url,
        media_size=media_size,
        media_type=media_type,
        media_duration_s=media_duration_s,
    )

    logger_ep.debug("Rendering poster")
    podcast_episode = PodcastEpisode(**data)
    # The _dirty set causes image cache miss as every time the set gets
    # pickled and serialized to string in different ordering. We won't be
    # saving this object to database, the only purpose is to provide
    # the image renderer with a populated Peewee model object, so let's drop
    # the contents.
    podcast_episode.clear_dirty_fields()
    tpl_context = dict(podcast_episode=podcast_episode)
    poster_path = render_image_file(
        POSTER_WIDTH,
        POSTER_HEIGHT,
        "podcast_episode.jinja",
        tpl_context,
        POSTERS_DIR,
        prefix=media_slug,
        filters=dict(icon=icon),
    )
    data["poster_path"] = poster_path.relative_to(IMAGES_DIR)

    return data


@db.connection_context()
async def announce_new_episode(client: ClubClient):
    last_episode = PodcastEpisode.last()
    last_message = ClubMessage.last_bot_message(
        ClubChannelID.ANNOUNCEMENTS,
        MESSAGE_EMOJI,
        f"**{last_episode.number}. epizodu**",
    )
    if not last_message:
        if last_episode.publish_on < (TODAY - timedelta(days=30 * 3)):
            logger.warning(f"Last episode {last_episode!r} is too old, not announcing")
            return
        logger.info(f"Announcing {last_episode!r}")
        channel = await client.fetch_channel(ClubChannelID.ANNOUNCEMENTS)
        content = (
            f"{MESSAGE_EMOJI} Nastraž uši! <@{ClubMemberID.PAVLINA}>"
            f" natočila **{last_episode.number}. epizodu** podcastu!"
        )

        description_embed = Embed(
            title=last_episode.format_title(number=True),
            description=last_episode.description.strip(),
            color=Color.yellow(),
        )
        description_embed.set_thumbnail(
            url=f"attachment://{Path(last_episode.poster_path).name}"
        )
        poster_file = File(IMAGES_DIR / last_episode.poster_path)

        details = (
            f"⏱️ {last_episode.media_duration_m} minut poslechu\n"
            f"<a:vincent:900831887591882782> Do půl hodiny to bude na webu, brzo potom i na ostatních službách\n"
        )
        details_embed = Embed(description=details)

        view = ui.View(
            ui.Button(
                emoji="<:juniorguru:841683119291760640>",
                label="web",
                url=last_episode.url,
            ),
            ui.Button(
                emoji="<:youtube:976200175490060299>",
                label="YouTube",
                url="https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA",
            ),
            ui.Button(
                emoji="<:spotify:1085596335794819092>",
                label="Spotify",
                url="https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4",
            ),
            ui.Button(
                emoji="<:appleinc:842465215718227987>",
                label="Apple",
                url="https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549",
            ),
        )
        with mutating_discord(channel) as proxy:
            await proxy.send(
                content=content,
                embeds=[description_embed, details_embed],
                files=[poster_file],
                view=view,
            )
    else:
        logger.info(f"Looks like {last_episode!r} has been already announced")
