import itertools
from asyncio import TaskGroup
from datetime import UTC, date, datetime, timedelta
from operator import attrgetter
from pathlib import Path
from typing import Annotated
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo

import click
import yaml
from discord import Embed
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    HttpUrl,
    PlainSerializer,
    computed_field,
    field_validator,
)

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, discord_task, loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubClient, add_reactions, parse_channel_link
from jg.coop.lib.location import REGIONS, locate
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.meetup import Meetup


YAML_PATH = Path("src/jg/coop/data/meetups.yml")


logger = loggers.from_path(__file__)


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")
    return dt.astimezone(UTC)


class MeetupData(BaseModel):
    title: Annotated[str, BeforeValidator(str.strip)]
    starts_at: Annotated[datetime, AfterValidator(to_utc)]
    ends_at: Annotated[datetime, AfterValidator(to_utc)]
    location: str
    region: str | None = None
    url: Annotated[HttpUrl, PlainSerializer(str)]
    series_name: str
    series_org: str
    series_url: Annotated[HttpUrl, PlainSerializer(str)]

    def model_dump_db(self) -> dict:
        data = self.model_dump()
        data["starts_at"] = self.starts_at.replace(tzinfo=None)
        data["ends_at"] = self.ends_at.replace(tzinfo=None)
        return data


class PostingInstruction(BaseModel):
    channel_id: int
    meetup: MeetupData


class ThreadConfig(YAMLConfig):
    url: HttpUrl
    regions: list[str]

    @computed_field
    def id(self) -> int:
        return parse_channel_link(str(self.url))

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: HttpUrl) -> HttpUrl:
        parse_channel_link(str(value))
        return value

    @field_validator("regions")
    @classmethod
    def validate_regions(cls, value: list[str]) -> list[str]:
        for region in value:
            if region not in REGIONS:
                raise ValueError(
                    f"Invalid region {region!r}, expected one of {REGIONS})"
                )
        return value


class MeetupsConfig(YAMLConfig):
    threads: list[ThreadConfig]


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--config",
    "config_path",
    default="src/jg/coop/data/meetups.yml",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--actor",
    "actor_names",
    multiple=True,
    default=[
        "honzajavorek/meetups-ctvrtkon",
        "honzajavorek/meetups-czjug",
        "honzajavorek/meetups-makerfaire",
        "honzajavorek/meetups-meetupcom",
        "honzajavorek/meetups-pehapkari",
        "honzajavorek/meetups-pyvo",
    ],
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--days", default=30, type=int)
@db.connection_context()
@async_command
async def main(config_path: Path, actor_names: list[str], today: date, days: int):
    logger.info("Setting up meetups db table")
    Meetup.drop_table()
    Meetup.create_table()

    logger.info(f"Reading {config_path.name}")
    yaml_data = yaml.safe_load(config_path.read_text())
    config = MeetupsConfig(**yaml_data)
    logger.info(f"Loaded {len(config.threads)} local groups")

    items = itertools.chain.from_iterable(
        apify.fetch_data(actor_name) for actor_name in actor_names
    )
    meetups = [MeetupData(**item) for item in items]
    logger.info(f"Fetched {len(meetups)} meetups")

    meetups = [
        meetup
        for meetup in meetups
        if (
            meetup.starts_at.date() >= today
            and meetup.starts_at.date() < today + timedelta(days=days)
        )
    ]
    logger.info(f"Found {len(meetups)} meetups in next {days} days")

    logger.info("Locating meetups")
    async with TaskGroup() as task_group:
        tasks = [task_group.create_task(locate(meetup.location)) for meetup in meetups]
    for meetup, task in zip(meetups, tasks):
        meetup.region = task.result().region

    logger.info("Saving meetups to the database")
    for meetup in meetups:
        Meetup.create(**meetup.model_dump_db())

    logger.info("Sorting meetups by region")
    meetups.sort(key=attrgetter("region"))
    meetups_by_region = {
        region: list(meetups)
        for region, meetups in itertools.groupby(meetups, key=attrgetter("region"))
    }
    stats = [
        f"{region} ({len(meetups)})" for region, meetups in meetups_by_region.items()
    ]
    logger.info(f"Meetups by region: {', '.join(stats)}")

    instructions = []
    for thread in config.threads:
        logger.info(f"Group {thread.url}: {', '.join(thread.regions)}")
        thread_meetups = sorted(
            itertools.chain.from_iterable(
                meetups_by_region.get(region, []) for region in thread.regions
            ),
            key=attrgetter("starts_at"),
        )
        logger.info(f"Found {len(thread_meetups)} relevant meetups")

        messages_since_at = datetime.combine(
            today - timedelta(days=2 * days), datetime.min.time()
        )
        messages_by_url = {
            message.ui_urls[0]: message
            for message in ClubMessage.channel_listing(
                thread.id, by_bot=True, since_at=messages_since_at
            )
            if message.ui_urls
        }
        logger.info(f"Found {len(messages_by_url)} bot messages with UI URLs")

        thread_meetups = [
            meetup
            for meetup in thread_meetups
            if str(meetup.url) not in messages_by_url
        ]
        logger.info(f"Will post {len(thread_meetups)} relevant meetups")
        instructions.extend(
            PostingInstruction(channel_id=thread.id, meetup=meetup)
            for meetup in thread_meetups
        )
    if instructions:
        discord_task.run(sync_meetups, instructions)


async def sync_meetups(client: ClubClient, instructions: list[PostingInstruction]):
    for instruction in instructions:
        channel = client.get_partial_messageable(instruction.channel_id)
        meetup = instruction.meetup
        with mutating_discord(channel) as proxy:
            embed = Embed(
                title=meetup.title,
                description=(
                    "Pojď ven a spolu s lidmi z klubu objevuj další komunity! "
                    f"Tuto akci pořádá **{meetup.series_org}**. "
                    "Pokud zvažuješ dorazit, dej 🙋 na tento příspěvek, "
                    "ať jde vidět, kdo všechno by možná šel."
                ),
                url=meetup.url,
            )
            embed.set_author(name=meetup.series_name, url=meetup.series_url)
            embed.add_field(
                name="🗓️ Kdy", value=format_time(meetup.starts_at, meetup.ends_at)
            )
            embed.add_field(
                name="📍 Kde",
                value=(
                    meetup.location
                    + (
                        f" ([Mapy.cz]({mapycz_url(meetup.location)}), "
                        f"[Google Mapy]({googlemaps_url(meetup.location)}))"
                    )
                ),
                inline=False,
            )
            logger.debug(
                (
                    f"Posting:\n- {embed.title!r}\n- {embed.url!r}"
                    f"\n- {embed.author.name!r}\n"
                )
                + "\n".join(
                    [f"- {field.name!r}: {field.value!r}" for field in embed.fields]
                )
            )
            message = await proxy.send(embed=embed)
        if message:
            await add_reactions(message, "🙋")


def format_time(
    starts_at: datetime, ends_at: datetime, tz: ZoneInfo = ZoneInfo("Europe/Prague")
) -> str:
    starts_at = starts_at.astimezone(tz)
    ends_at = ends_at.astimezone(tz)
    if starts_at.date() == ends_at.date():
        return f"{weekday(starts_at)} {starts_at:%-d.%-m. %H:%M} až {ends_at:%H:%M}"
    return (
        f"{weekday(starts_at)} "
        f"{starts_at:%-d.%-m. %H:%M} až "
        f"{weekday(ends_at)} "
        f"{ends_at:%-d.%-m. %H:%M}"
    )


def weekday(dt: datetime) -> str:
    return ["neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota"][
        int(dt.strftime("%w"))
    ]


def mapycz_url(location: str) -> str:
    return f"https://mapy.cz/?q={quote_plus(location)}"


def googlemaps_url(location: str) -> str:
    return f"https://www.google.com/maps?q={quote_plus(location)}"
