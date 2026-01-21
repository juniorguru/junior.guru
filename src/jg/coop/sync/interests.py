from pathlib import Path
from typing import Literal

import click
import httpx
import yaml
from discord import ChannelType, Thread
from discord.errors import Forbidden
from pydantic import BaseModel, HttpUrl, computed_field, field_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import (
    CLUB_GUILD_ID,
    ClubChannelID,
    ClubClient,
    parse_channel_link,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.club import ClubChannel, ClubMessage, ClubUser
from jg.coop.models.role import InterestRole


logger = loggers.from_path(__file__)


YAML_PATH = Path("src/jg/coop/data/interests.yml")

IMAGES_DIR = Path("src/jg/coop/images")

ICONS_DIR = IMAGES_DIR / "interests"

EMOJI = "🛹"

ICON_URLS = {
    "devicon": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{slug}/{slug}-plain.svg",
    "bootstrap": "https://icons.getbootstrap.com/assets/icons/{slug}.svg",
}


class MemberInterests(BaseModel):
    member_id: int
    dm_channel_id: int
    role_names: list[str]
    thread_ids: list[int]


class IconConfig(YAMLConfig):
    set: Literal["devicon", "bootstrap"]
    slug: str


class RoleConfig(YAMLConfig):
    id: int
    icon: IconConfig
    threads: list[HttpUrl]

    @computed_field
    def threads_ids(self) -> list[int]:
        return [parse_channel_link(str(thread_url)) for thread_url in self.threads]

    @field_validator("threads")
    @classmethod
    def validate_threads(cls, value: list[HttpUrl]) -> list[HttpUrl]:
        for url in value:
            parse_channel_link(str(url))
        return value


class InterestsConfig(YAMLConfig):
    roles: list[RoleConfig]


@cli.sync_command(dependencies=["club-content", "roles"])
@click.option(
    "--config",
    "config_path",
    default="src/jg/coop/data/interests.yml",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--tag", default="zájmová skupinka")
@click.option("--debug-user", default=None, type=int)
@db.connection_context()
@async_command
async def main(config_path: Path, tag: str, debug_user: int | None):
    # Load configuration
    logger.info(f"Reading {config_path.name}")
    yaml_data = yaml.safe_load(config_path.read_text())
    config = InterestsConfig(**yaml_data)
    logger.info(f"Loaded {len(config.roles)} interest role configs")

    # Validate roles configuration against database and save thread IDs
    config_roles = {role.id: role for role in config.roles}
    interest_roles: dict[int, InterestRole] = {}
    for role in InterestRole.listing():
        if role.club_id in config_roles:
            role.threads_ids = config_roles[role.club_id].threads_ids
            role.save()
            logger.info(f"Role configured: {role.interest_name}")
            interest_roles[role.club_id] = role
        else:
            logger.warning(f"Role not configured: {role.interest_name}")
    if extra_ids := set(config_roles) - set(interest_roles):
        raise ValueError(f"Configured interest roles not found: {extra_ids}")

    # Ensure roles have icons
    async with httpx.AsyncClient() as http_client:
        for role_id, role in interest_roles.items():
            icon_path = ICONS_DIR / f"{role_id}.svg"
            if icon_path.exists():
                logger.debug(f"Icon already exists: {icon_path}")
            else:
                config_icon = config_roles[role_id].icon
                icon_url = ICON_URLS[config_icon.set].format(slug=config_icon.slug)
                logger.info(f"Fetching {role.interest_name!r} icon from {icon_url}")
                response = await http_client.get(icon_url)
                response.raise_for_status()
                icon_path.write_bytes(response.content)
            role.icon_path = icon_path.relative_to(IMAGES_DIR)
            role.save()

    # Validate threads configuration against database
    config_thread_ids = {
        thread_id for role in config.roles for thread_id in role.threads_ids
    }
    interest_threads: dict[int, ClubChannel] = {}
    for channel in ClubChannel.tag_listing(tag):
        if channel.id in config_thread_ids:
            logger.info(f"Thread configured: {channel.name} #{channel.id}")
            interest_threads[channel.id] = channel
        else:
            logger.warning(f"Thread not configured: {channel.name} #{channel.id}")
    if extra_ids := config_thread_ids - set(interest_threads):
        raise ValueError(f"Configured interest threads not found: {extra_ids}")

    # Members to go through
    if debug_user:
        logger.warning(f"DEBUG MODE enabled, processing only member #{debug_user}!")
        members = [ClubUser.get_by_id(debug_user)]
    else:
        members = ClubUser.members_listing()

    # Check what needs to be done
    members_interests: list[MemberInterests] = []
    for member in members:
        member_roles_ids = set(member.initial_roles) & set(config_roles)

        # Any relevant roles at all?
        if not member_roles_ids:
            continue

        # Figure out member roles
        member_config_roles = [config_roles[role_id] for role_id in member_roles_ids]
        member_roles = [interest_roles[role_id] for role_id in member_roles_ids]
        member_role_names = [role.interest_name for role in member_roles]
        logger.debug(f"Member #{member.id} interests: {member_role_names}")

        # Figure out member threads
        member_threads_ids = {
            thread_id
            for config_role in member_config_roles
            for thread_id in config_role.threads_ids
        }
        member_threads = [
            interest_threads[thread_id] for thread_id in member_threads_ids
        ]
        member_threads.sort(key=lambda thread: thread.name.lower())
        logger.debug(
            f"Member #{member.id} threads: {[thread.name for thread in member_threads]}"
        )
        if not member_threads:
            logger.info(
                f"Member #{member.id} interests {member_role_names} have no configured threads, skipping"
            )
            continue

        # Figure out what relevant messages the member has in their DM channel
        messages = ClubMessage.channel_listing(
            member.dm_channel_id, starting_emoji=EMOJI, by_bot=True
        )
        logger.debug(f"Member #{member.id} has relevant DM messages: {len(messages)}")

        if has_info_message(messages):
            logger.info(
                f"Member #{member.id} already informed about interest threads, skipping"
            )
            continue

        logger.info(
            f"Member #{member.id} with interests {member_role_names} "
            f"will receive info about threads {[thread.name for thread in member_threads]}"
        )
        members_interests.append(
            MemberInterests(
                member_id=member.id,
                dm_channel_id=member.dm_channel_id,
                role_names=member_role_names,
                thread_ids=[thread.id for thread in member_threads],
            )
        )
    if members_interests:
        discord_task.run(sync_interests, members_interests)


async def sync_interests(client: ClubClient, members_interests: list[MemberInterests]):
    thread_ids = {
        thread_id
        for member_interests in members_interests
        for thread_id in member_interests.thread_ids
    }
    threads = {
        thread_id: (
            client.club_guild.get_thread(thread_id)
            or await client.club_guild.fetch_channel(thread_id)
        )
        for thread_id in thread_ids
    }
    dm_channels = {
        id: client.get_partial_messageable(id, type=ChannelType.private)
        for id in {
            member_interests.dm_channel_id for member_interests in members_interests
        }
    }
    for member_interests in members_interests:
        dm_channel = dm_channels[member_interests.dm_channel_id]
        member_threads = [
            threads[thread_id] for thread_id in member_interests.thread_ids
        ]
        logger.info(
            f"Informing member #{member_interests.member_id} about "
            f"{len(member_interests.role_names)} roles and "
            f"{len(member_threads)} threads"
        )
        with mutating_discord(dm_channel) as proxy:
            try:
                await proxy.send(
                    create_message(member_interests.role_names, member_threads)
                )
            except Forbidden as e:
                logger.error(
                    f"Cannot send DM to member #{member_interests.member_id}: {e}"
                )


def create_message(role_names: list[str], threads: list[Thread], limit=5) -> str:
    threads_count = len(threads)
    if threads_count > limit:
        threads = threads[:limit]
        threads_text = f"{format_threads(threads)}\n\n(a další, celkem {threads_count})"
    else:
        threads_text = format_threads(threads)
    return (
        f"{EMOJI} Podle tvých zájmů to vypadá, že by tě mohly bavit tyhle vlákna:"
        f"\n\n{threads_text}\n\n"
        f"Jak jsem na to přišlo? Máš tyto zájmové role: {', '.join(role_names)}. "
        "Můžeš si je změnit v sekci **Kanály a role**, která je v klubu úplně nahoře v seznamu kanálů."
        "\n\n"
        "Teď zpět k těm vláknům. Jsou to „zájmové skupinky”. "
        "Jakmile do nich někdo přispěje, **automaticky tě přidám**. "
        "Každé vlákno má ale v záhlaví tlačítko _Sledující_ (_Following_), kterým se můžeš kdykoliv odhlásit."
        "\n\n"
        "Sdílí se v nich novinky, drby, tipy, filozofické úvahy, vysvětlují obecnější koncepty, nebo řeší společné úlohy."
        "Pokud něco vyloženě debuguješ, je lepší tím skupinky nespamovat. "
        f"Založ si to v poradně https://discord.com/channels/{CLUB_GUILD_ID}/{ClubChannelID.QA} "
        "a do vhodné skupinky pak na něho dej pouze odkaz."
    )


def format_threads(threads: list[Thread]) -> str:
    return "\n".join(
        f"**{thread.name}**\nOdkaz: {thread.jump_url}" for thread in threads
    )


def has_info_message(messages: list[ClubMessage]) -> bool:
    return any(message.content.startswith(EMOJI) for message in messages)
