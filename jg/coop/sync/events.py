from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Annotated, Any, TypedDict
from zoneinfo import ZoneInfo

import click
import yaml
from discord import ScheduledEvent
from pydantic import (
    AfterValidator,
    BeforeValidator,
    HttpUrl,
    PlainSerializer,
)

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    CLUB_GUILD_ID,
    ClubChannelID,
    ClubClient,
    ClubMemberID,
    add_reactions,
    parse_channel,
    parse_discord_link,
)
from jg.coop.lib.images import (
    PostersCache,
    is_image,
    render_image_file,
    validate_image,
)
from jg.coop.lib.mutations import MutationsNotAllowedError, mutating_discord
from jg.coop.lib.template_filters import icon, local_time, weekday
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.event import Event, EventSpeaking
from jg.coop.sync.club_content.crawler import CHANNELS_HISTORY_SINCE


logger = loggers.from_path(__file__)


EVENTS_YAML_PATH = Path("jg/coop/data/events.yml")

IMAGES_DIR = Path("jg/coop/images")

POSTERS_DIR = IMAGES_DIR / "posters-events"

AVATARS_DIR = IMAGES_DIR / "avatars-participants"

ANNOUNCEMENT_EMOJIS = [
    "👀",
    "🤩",
    "😍",
    "👍",
    "📺",
    "🍿",
    "<a:yayfrog:976193164471853097>",
]


def check_time(value: str) -> str:
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValueError("The time must be in the format HH:MM")
    return value


def get_avatar_path(value: Any) -> Path:
    image_path = IMAGES_DIR / value
    if image_path.exists():
        return image_path
    raise ValueError(f"Path doesn't exist: {image_path!r}")


def check_club_recording_url(value: HttpUrl) -> HttpUrl:
    discord_ids = parse_discord_link(str(value))
    if discord_ids["guild_id"] != CLUB_GUILD_ID:
        raise ValueError(f"The club recording URL {value} doesn't lead to the club")
    if discord_ids["channel_id"] not in CHANNELS_HISTORY_SINCE:
        raise ValueError(
            f"The club recording URL {value} doesn't lead to a channel with fully crawled history"
        )
    if CHANNELS_HISTORY_SINCE[discord_ids["channel_id"]] is not None:
        raise ValueError(
            f"The club recording URL {value} doesn't lead to a channel with fully crawled history"
        )
    return value


class EventConfig(YAMLConfig):
    id: int
    title: str
    date: date
    time: Annotated[str, AfterValidator(check_time)] | None = "18:00"
    expected_duration_h: float = 1.5
    description: str
    short_description: str | None = None
    avatar_path: Annotated[Path, BeforeValidator(get_avatar_path)] | None = None
    bio_name: str
    bio_title: str | None = None
    bio: str
    bio_links: list[str] = []
    club_speaker_ids: list[int] = []
    club_recording_url: (
        Annotated[
            HttpUrl,
            AfterValidator(check_club_recording_url),
            PlainSerializer(str),
        ]
        | None
    ) = None
    public_recording_url: Annotated[HttpUrl, PlainSerializer(str)] | None = None


class EventsConfig(YAMLConfig):
    registry: list[EventConfig]


class EventStartEnd(TypedDict):
    start_at: datetime
    end_at: datetime


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--announcements-channel",
    "announcements_channel_id",
    default="announcements",
    type=parse_channel,
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--clear-posters/--keep-posters", default=False)
@click.option("--width", default=1280, type=int)
@click.option("--height", default=720, type=int)
def main(
    announcements_channel_id: int,
    today: date,
    clear_posters: bool,
    width: int,
    height: int,
):
    posters = PostersCache(POSTERS_DIR)
    posters.init(clear=clear_posters)

    logger.info("Validating avatar images")
    for path in filter(is_image, AVATARS_DIR.glob("*.*")):
        logger.debug(f"Validating {path}")
        validate_image(path)

    with db.connection_context():
        logger.info("Setting up events db tables")
        db.drop_tables([Event, EventSpeaking])
        db.create_tables([Event, EventSpeaking])

        logger.info("Processing data from the YAML, creating posters")
        events_config = EventsConfig(**yaml.safe_load(EVENTS_YAML_PATH.read_text()))
        for event_config in events_config.registry:
            logger.info(f"Creating event: {event_config.title!r}")
            event = Event.create(**prepare_event_data(event_config))
            for speaker_id in event_config.club_speaker_ids:
                logger.info(f"Marking member #{speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event)

            logger.info(f"Rendering posters for {event_config.title!r}")
            image_path = render_image_file(
                width,
                height,
                "thumbnail.jinja",
                dict(
                    title=event.title,
                    image_path=event.avatar_path,
                    subheading=event.bio_name,
                    date=event.start_at,
                    button_heading="Sleduj na",
                    button_link=(
                        "youtube.com/@juniordotguru"
                        if event.public_recording_url
                        else "junior.guru/events"
                    ),
                ),
                POSTERS_DIR,
                filters=dict(local_time=local_time, weekday=weekday, icon=icon),
                prefix=event.start_at.date().isoformat().replace("-", ""),
            )
            image_path_relative = image_path.relative_to(IMAGES_DIR)
            event.poster_path = image_path_relative
            posters.record(IMAGES_DIR / image_path_relative)

            logger.info(f"Saving {event_config.title!r}")
            event.save()
    posters.cleanup()

    logger.info("Syncing with Discord")
    discord_task.run(sync_scheduled_events)
    discord_task.run(post_next_event_messages, today, announcements_channel_id)


@db.connection_context()
async def sync_scheduled_events(client: ClubClient):
    discord_events = {
        scheduled_event.start_time.replace(tzinfo=None): scheduled_event
        for scheduled_event in client.club_guild.scheduled_events
        if is_event_scheduled_event(scheduled_event)
    }
    channel = await client.fetch_channel(ClubChannelID.EVENTS)
    for event in Event.planned_listing():
        discord_event = discord_events.get(event.start_at)
        try:
            if discord_event:
                logger.info(
                    f"Discord event for '{event.title}' already exists, updating"
                )
                with mutating_discord(discord_event, raises=True) as proxy:
                    discord_event = await proxy.edit(
                        name=event.full_title,
                        description=event.discord_description,
                        end_time=event.end_at,
                        cover=(IMAGES_DIR / event.poster_path).read_bytes(),
                    )
            else:
                logger.info(f"Creating Discord event for '{event.title}'")
                with mutating_discord(client.club_guild, raises=True) as proxy:
                    discord_event = await proxy.create_scheduled_event(
                        name=event.full_title,
                        description=event.discord_description,
                        start_time=event.start_at,
                        end_time=event.end_at,
                        location=channel,
                    )
        except MutationsNotAllowedError:
            pass
        if discord_event:
            event.club_event_id = discord_event.id
            event.club_event_url = discord_event.url
            event.save()


def is_event_scheduled_event(scheduled_event: ScheduledEvent) -> bool:
    # Since October 2023 the creator_id is always None, it's
    # a Discord bug: https://github.com/discord/discord-api-docs/issues/6481
    # Checking if it's created by the bot only if it's not None should be future proof.
    if (
        scheduled_event.creator_id is not None
        and int(scheduled_event.creator_id) != ClubMemberID.BOT
    ):
        return False
    location_id = getattr(scheduled_event.location.value, "id", None)
    return location_id == ClubChannelID.EVENTS


@db.connection_context()
async def post_next_event_messages(
    client: ClubClient, today: date, announcements_channel_id: int
):
    announcements_channel = await client.fetch_channel(announcements_channel_id)
    events_channel = await client.fetch_channel(ClubChannelID.EVENTS)

    for event in Event.planned_listing():
        logger.info(f"Processing event {event.title!r}")
        speakers = ", ".join(
            [speaking.speaker.mention for speaking in event.list_speaking]
        )
        speakers = speakers or event.bio_name

        logger.info("About to post a message on the day when the event is")
        if event.start_at.date() == today:
            message = ClubMessage.last_bot_message(
                announcements_channel_id, "⏰", event.discord_url
            )
            if message:
                logger.info(
                    f"Looks like the message about {event.discord_url} already exists: {message.url}"
                )
            else:
                logger.info("Found no message, posting!")
                content = f"⏰ @everyone Už **dnes v {event.start_at_prg:%H:%M}** bude v klubu akce „{event.title}” s {speakers}! Odehrávat se to bude v {events_channel.mention}, dotazy jde pokládat v tamním chatu 💬 Akce se nahrávají, odkaz na záznam se objeví v tomto kanálu. {event.discord_url}"
                with mutating_discord(announcements_channel) as proxy:
                    discord_message = await proxy.send(content)
                if discord_message:
                    with mutating_discord(discord_message) as proxy:
                        await add_reactions(
                            discord_message, ["⏰"] + ANNOUNCEMENT_EMOJIS
                        )
        else:
            logger.info("It's not the day when the event is")
            logger.info("About to post a message 1 day prior to the event")
            if event.start_at.date() - timedelta(days=1) == today:
                message = ClubMessage.last_bot_message(
                    announcements_channel_id, "🤩", event.discord_url
                )
                if message:
                    logger.info(
                        f"Looks like the message about {event.discord_url} already exists: {message.url}"
                    )
                else:
                    logger.info("Found no message, posting!")
                    content = f"🤩 Už **zítra v {event.start_at_prg:%H:%M}** bude v klubu akce „{event.title}” s {speakers}! {event.discord_url}"
                    with mutating_discord(announcements_channel) as proxy:
                        discord_message = await proxy.send(content)
                    if discord_message:
                        with mutating_discord(discord_message) as proxy:
                            await add_reactions(
                                discord_message, ["✨"] + ANNOUNCEMENT_EMOJIS
                            )
            else:
                logger.info("It's not 1 day prior to the event")
                logger.info("About to post a message 7 days prior to the event")
                if event.start_at.date() - timedelta(days=7) <= today:
                    message = ClubMessage.last_bot_message(
                        announcements_channel_id, "🗓", event.discord_url
                    )
                    if message:
                        logger.info(
                            f"Looks like the message about {event.discord_url} already exists: {message.url}"
                        )
                    else:
                        logger.info("Found no message, posting!")
                        content = f"🗓 Už **za týden** bude v klubu akce „{event.title}” s {speakers}! {event.discord_url}"
                        with mutating_discord(announcements_channel) as proxy:
                            discord_message = await proxy.send(content)
                        if discord_message:
                            with mutating_discord(discord_message) as proxy:
                                await add_reactions(
                                    discord_message, ["🗓"] + ANNOUNCEMENT_EMOJIS
                                )
                else:
                    logger.info("It's not 7 days prior to the event")

        # See https://github.com/Pycord-Development/pycord/issues/1934
        #
        # logger.info("About to post a message to event chat on the day when the event is")
        # if event.start_at.date() == today:
        #     message = ClubMessage.last_bot_message(ClubChannelID.EVENTS, '👋', event.discord_url)
        #     if message:
        #         logger.info(f'Looks like the message already exists: {message.url}')
        #     else:
        #         logger.info("Found no message, posting!")
        #         content = [
        #             f"👋 Už **dnes v {event.start_at_prg:%H:%M}** tady bude probíhat „{event.title}” s {speakers} (viz {announcements_channel.mention}). Tento kanál slouží k pokládání dotazů, sdílení odkazů, slajdů k prezentaci…",
        #             "",
        #             "⚠️ Ve výchozím nastavení Discord udělá zvuk při každé aktivitě v hlasovém kanálu, např. při připojení nového účastníka, odpojení, vypnutí zvuku, zapnutí, apod. Zvuky si vypni v Uživatelských nastaveních (_User Settings_), na stránce Oznámení (_Notifications_), sekce Zvuky (_Sounds_). Většina zvuků souvisí s hovory, takže je potřeba povypínat skoro vše.",
        #             "",
        #             f"📺 Limit přímých účastníků je 25, takže přijďte včas. Kdo se nevleze, bude mít možnost sledovat stream na YouTube, odkaz se kdyžtak objeví tady v chatu. Záznam se po akci objeví v {announcements_channel.mention}.",
        #             "",
        #             f"ℹ️ {event.description_plain}",
        #             "",
        #             f"🦸 {event.bio_plain}"
        #             "",
        #             "",
        #             f"👉 {event.url}",
        #         ]
        #         with mutating_discord(events_channel) as proxy:
        #             await proxy.send('\n'.join(content))
        # else:
        #     logger.info("It's not the day when the event is")


def prepare_event_data(event_config: EventConfig) -> dict[str, Any]:
    event_data = event_config.model_dump(
        exclude=[
            "date",
            "time",
            "expected_duration_h",
            "avatar_path",
            "club_speaker_ids",
        ]
    )
    event_data |= get_event_start_end(event_config)
    if event_config.avatar_path:
        event_data["avatar_path"] = event_config.avatar_path.relative_to(IMAGES_DIR)
    return event_data


def get_event_start_end(event_config: EventConfig) -> EventStartEnd:
    start_at_prg = datetime(
        *map(int, str(event_config.date).split("-")),
        *map(int, event_config.time.split(":")),
        tzinfo=ZoneInfo("Europe/Prague"),
    )
    start_at_utc = start_at_prg.astimezone(UTC)
    start_at = start_at_utc.replace(tzinfo=None)
    return EventStartEnd(
        start_at=start_at,
        end_at=start_at + timedelta(hours=event_config.expected_duration_h),
    )
