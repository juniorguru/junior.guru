import itertools
from asyncio import TaskGroup
from datetime import date, datetime, timedelta
from operator import attrgetter
from pathlib import Path
from urllib.parse import quote_plus

import click
import yaml
from discord import Embed
from pydantic import BaseModel, HttpUrl, computed_field, field_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, discord_task, loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubClient, add_reactions, parse_link
from jg.coop.lib.mapycz import REGIONS, locate
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage


YAML_PATH = Path("jg/coop/data/meetups.yml")


logger = loggers.from_path(__file__)


class Meetup(BaseModel):
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str
    region: str | None = None
    url: HttpUrl
    series_name: str
    series_org: str
    series_url: HttpUrl


class PostingInstruction(BaseModel):
    channel_id: int
    meetup: Meetup


class GroupConfig(YAMLConfig):
    group_url: HttpUrl
    regions: list[str]

    @computed_field
    @property
    def channel_id(self) -> int:
        return parse_channel_id(self.group_url)

    @field_validator("group_url")
    @classmethod
    def validate_group_url(cls, value: HttpUrl) -> HttpUrl:
        parse_channel_id(value)
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
    groups: list[GroupConfig]


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--config",
    "config_path",
    default="jg/coop/data/meetups.yml",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--actor",
    "actor_names",
    multiple=True,
    default=[
        "honzajavorek/meetups-meetupcom",
        "honzajavorek/meetups-pyvo",
        "honzajavorek/meetups-ctvrtkon",
        "honzajavorek/meetups-czjug",
        "honzajavorek/meetups-pehapkari",
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
    logger.info(f"Reading {config_path.name}")
    yaml_data = yaml.safe_load(config_path.read_text())
    config = MeetupsConfig(**yaml_data)
    logger.info(f"Loaded {len(config.groups)} local groups")

    items = itertools.chain.from_iterable(
        apify.fetch_data(actor_name) for actor_name in actor_names
    )
    meetups = [Meetup(**item) for item in items]
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
    for group in config.groups:
        logger.info(f"Group {group.group_url}: {', '.join(group.regions)}")
        group_meetups = sorted(
            itertools.chain.from_iterable(
                meetups_by_region.get(region, []) for region in group.regions
            ),
            key=attrgetter("starts_at"),
        )
        logger.info(f"Found {len(group_meetups)} relevant meetups")

        messages_by_url = {
            message.ui_urls[0]: message
            for message in ClubMessage.channel_listing(group.channel_id, by_bot=True)
            if message.ui_urls
        }
        logger.info(f"Found {len(messages_by_url)} bot messages with UI URLs")

        group_meetups = [
            meetup for meetup in group_meetups if str(meetup.url) not in messages_by_url
        ]
        logger.info(f"Will post {len(group_meetups)} relevant meetups")
        instructions.extend(
            PostingInstruction(channel_id=group.channel_id, meetup=meetup)
            for meetup in group_meetups
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
                    "Kdo chcete jít, dejte 🙋 na tento příspěvek."
                ),
                url=meetup.url,
            )
            embed.set_author(name=meetup.series_name, url=meetup.series_url)
            embed.add_field(name="🗓️ Kdy", value=format_time(meetup))
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


def parse_channel_id(url: str | HttpUrl) -> int:
    try:
        return parse_link(str(url))["channel_id"]
    except KeyError:
        raise ValueError(f"Invalid Discord channel URL: {url}")


def format_time(meetup: Meetup) -> str:
    if meetup.starts_at.date() == meetup.ends_at.date():
        return (
            f"{weekday(meetup.starts_at)} "
            f"{meetup.starts_at:%-d.%-m. %H:%M} až "
            f"{meetup.ends_at:%H:%M}"
        )
    return (
        f"{weekday(meetup.starts_at)} "
        f"{meetup.starts_at:%-d.%-m. %H:%M} až "
        f"{weekday(meetup.ends_at)} "
        f"{meetup.ends_at:%-d.%-m. %H:%M}"
    )


def weekday(dt: datetime) -> str:
    return ["neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota"][
        int(dt.strftime("%w"))
    ]


def mapycz_url(location: str) -> str:
    return f"https://mapy.cz/?q={quote_plus(location)}"


def googlemaps_url(location: str) -> str:
    return f"https://www.google.com/maps?q={quote_plus(location)}"
