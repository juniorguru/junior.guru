from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import click
from discord import ScheduledEvent
from strictyaml import CommaSeparated, Float, Int, Map, Optional, Seq, Str, Url, load

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import (
    ClubChannelID,
    ClubClient,
    ClubMemberID,
    add_reactions,
    parse_channel,
)
from jg.coop.lib.images import (
    PostersCache,
    is_image,
    render_image_file,
    validate_image,
)
from jg.coop.lib.mutations import MutationsNotAllowedError, mutating_discord
from jg.coop.lib.template_filters import icon, local_time, weekday
from jg.coop.lib.yaml import Date
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.event import Event, EventSpeaking


logger = loggers.from_path(__file__)


DATA_PATH = Path("jg/coop/data/events.yml")

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


schema = Seq(
    Map(
        {
            "id": Int(),
            "title": Str(),
            "date": Date(),
            Optional("time", default="18:00"): Str(),
            Optional("duration", default=1.5): Float(),
            "description": Str(),
            Optional("short_description"): Str(),
            Optional("avatar_path"): Str(),
            "bio_name": Str(),
            Optional("bio_title"): Str(),
            "bio": Str(),
            Optional("bio_links"): Seq(Str()),
            Optional("logo_path"): Str(),
            "speakers": CommaSeparated(Int()),
            Optional("recording_url"): Url(),
            Optional("public_recording_url"): Url(),
        }
    )
)


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
        records = [
            load_record(record.data) for record in load(DATA_PATH.read_text(), schema)
        ]
        for record in records:
            name = record["title"]
            logger.info(f"Creating '{name}'")
            speakers_ids = record.pop("speakers", [])
            event = Event.create(**record)

            for speaker_id in speakers_ids:
                logger.info(f"Marking member #{speaker_id} as a speaker")
                EventSpeaking.create(speaker=speaker_id, event=event)

            logger.debug(f"Checking '{event.avatar_path}'")
            image_path = IMAGES_DIR / event.avatar_path
            if not image_path.exists():
                raise ValueError(
                    f"Event '{name}' references '{image_path}', but it doesn't exist"
                )

            if event.logo_path:
                logger.debug(f"Checking '{event.logo_path}'")
                image_path = IMAGES_DIR / event.logo_path
                if not image_path.exists():
                    raise ValueError(
                        f"Event '{name}' references '{image_path}', but it doesn't exist"
                    )

            logger.info(f"Rendering posters for '{name}'")
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
            event.poster_dc_path = image_path_relative
            event.poster_yt_path = image_path_relative
            posters.record(IMAGES_DIR / image_path_relative)
            logger.info(f"Saving '{name}'")
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
                        cover=(IMAGES_DIR / event.poster_dc_path).read_bytes(),
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
            event.discord_id = discord_event.id
            event.discord_url = discord_event.url
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


def load_record(record):
    start_at_prg = datetime(
        *map(int, str(record.pop("date")).split("-")),
        *map(int, record.pop("time").split(":")),
        tzinfo=ZoneInfo("Europe/Prague"),
    )
    start_at_utc = start_at_prg.astimezone(UTC)
    start_at = start_at_utc.replace(tzinfo=None)
    record["start_at"] = start_at
    record["end_at"] = start_at + timedelta(hours=record.pop("duration"))
    return record
