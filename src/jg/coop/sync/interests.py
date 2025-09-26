from email.policy import default
from enum import StrEnum
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import Generator

import click
import discord
import yaml
from discord import ChannelType, Thread
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


YAML_PATH = Path("src/jg/coop/data/interests.yml")


logger = loggers.from_path(__file__)


EMOJI_NAMESPACE = "🛹"

EMOJI_ADD = "👋"

EMOJI_INFO = "<a:awkward:985064290044223488>"


class MembershipOperation(StrEnum):
    ADD = "add"
    INFO = "info"


class MembershipInstruction(BaseModel):
    member_id: int
    dm_channel_id: int
    operation: MembershipOperation
    thread_id: int


class RoleConfig(YAMLConfig):
    id: int
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
    type=click.Path(exists=True, path_type=Path),
)
@click.option("--tag", default="zájmová skupinka")
@click.option("--debug-user", default=None, type=int)
@db.connection_context()
@async_command
async def main(config_path: Path, tag: str, debug_user: int | None):
    logger.info(f"Reading {config_path.name}")
    yaml_data = yaml.safe_load(config_path.read_text())
    config = InterestsConfig(**yaml_data)
    logger.info(f"Loaded {len(config.roles)} interest role configs")

    # Validate roles configuration against database
    config_roles = {role.id: role for role in config.roles}
    interest_roles: dict[int, InterestRole] = {}
    for role in InterestRole.listing():
        if role.club_id in config_roles:
            logger.info(f"Role configured: {role.interest_name}")
            interest_roles[role.club_id] = role
        else:
            logger.warning(f"Role not configured: {role.interest_name}")
    if extra_ids := set(config_roles) - set(interest_roles):
        raise ValueError(f"Configured interest roles not found: {extra_ids}")

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

    # Members to process
    if debug_user:
        logger.warning(f"DEBUG MODE enabled, processing only member #{debug_user}!")
        members = [ClubUser.get_by_id(debug_user)]
    else:
        members = ClubUser.members_listing()

    # Check what needs to be done
    instructions = []
    for member in members:
        member_roles_ids = set(member.initial_roles) & set(config_roles)

        # Any relevant roles at all?
        if not member_roles_ids:
            continue

        # Figure out member roles
        member_config_roles = [config_roles[role_id] for role_id in member_roles_ids]
        member_roles = [interest_roles[role_id] for role_id in member_roles_ids]
        logger.debug(
            f"Member #{member.id} interests: {[role.interest_name for role in member_roles]}"
        )

        # Figure out member threads
        member_threads_ids = {
            thread_id
            for config_role in member_config_roles
            for thread_id in config_role.threads_ids
        }
        member_threads = [
            interest_threads[thread_id] for thread_id in member_threads_ids
        ]
        logger.debug(
            f"Member #{member.id} threads: {[thread.name for thread in member_threads]}"
        )

        # Figure out in which threads the member is missing
        member_threads_missing = [
            member_thread
            for member_thread in member_threads
            if member.id not in member_thread.members_ids
        ]
        if not member_threads_missing:
            continue
        logger.info(
            f"Member #{member.id} with interests {[role.interest_name for role in member_roles]} "
            f"is missing threads {[thread.name for thread in member_threads_missing]}"
        )

        # Figure out what relevant messages the member has in their DM channel
        messages = ClubMessage.channel_listing(
            member.dm_channel_id, starting_emoji=EMOJI_NAMESPACE, by_bot=True
        )
        logger.debug(f"Member #{member.id} has relevant DM messages: {len(messages)}")

        # Decide what to do with each thread the member is missing
        for member_thread in member_threads_missing:
            if contains_adding_message(messages, member_thread.url):
                if contains_info_message(messages, member_thread.url):
                    logger.info(
                        f"Member #{member.id} already informed about thread {member_thread.name} #{member_thread.id}, skipping"
                    )
                else:
                    logger.info(
                        f"Member #{member.id} will be only informed about {member_thread.name}"
                    )
                    instructions.append(
                        MembershipInstruction(
                            member_id=member.id,
                            dm_channel_id=member.dm_channel_id,
                            operation=MembershipOperation.INFO,
                            thread_id=member_thread.id,
                        )
                    )
            else:
                logger.info(
                    f"Member #{member.id} will be added to {member_thread.name}"
                )
                instructions.append(
                    MembershipInstruction(
                        member_id=member.id,
                        dm_channel_id=member.dm_channel_id,
                        operation=MembershipOperation.ADD,
                        thread_id=member_thread.id,
                    )
                )
    if instructions:
        discord_task.run(sync_interests, instructions)


async def sync_interests(client: ClubClient, instructions: list[MembershipInstruction]):
    threads = {
        id: (
            client.club_guild.get_thread(id)
            or await client.club_guild.fetch_channel(id)
        )
        for id in {instruction.thread_id for instruction in instructions}
    }
    dm_channels = {
        id: client.get_partial_messageable(id, type=ChannelType.private)
        for id in {instruction.dm_channel_id for instruction in instructions}
    }

    for member_id, dm_channel_id, member_instructions in group_by_member(instructions):
        logger.info(
            f"Processing member #{member_id}: {len(member_instructions)} instructions"
        )
        dm_channel = dm_channels[dm_channel_id]

        for op, op_instructions in group_by_operation(member_instructions):
            logger.info(f"Operation {op.value}: {len(op_instructions)} instructions")
            op_threads = [
                threads[instruction.thread_id] for instruction in op_instructions
            ]
            if op == MembershipOperation.ADD:
                for op_thread in op_threads:
                    logger.info(
                        f"Adding member #{member_id} to thread: {op_thread.name}"
                    )
                    with mutating_discord(op_thread) as proxy:
                        await proxy.add_user(discord.Object(id=member_id))
                with mutating_discord(dm_channel) as proxy:
                    await proxy.send(create_adding_message(op_threads))
            elif op == MembershipOperation.INFO:
                logger.info(
                    f"Informing member #{member_id} about {len(op_threads)} threads"
                )
                with mutating_discord(dm_channel) as proxy:
                    await proxy.send(create_info_message(op_threads))
            else:
                raise ValueError(f"Unknown operation: {op}")


def group_by_member(
    instructions: list[MembershipInstruction],
) -> Generator[tuple[int, int, list[MembershipInstruction]], None, None]:
    for member_id, member_instructions in groupby(
        sorted(instructions, key=attrgetter("member_id")),
        key=attrgetter("member_id"),
    ):
        member_instructions = list(member_instructions)
        dm_channel_ids = {
            instruction.dm_channel_id for instruction in member_instructions
        }
        if len(dm_channel_ids) != 1:
            raise ValueError(
                f"Multiple DM channels for member #{member_id}: {dm_channel_ids}"
            )
        yield member_id, dm_channel_ids.pop(), list(member_instructions)


def group_by_operation(
    instructions: list[MembershipInstruction],
) -> Generator[tuple[MembershipOperation, list[MembershipInstruction]], None, None]:
    for op, op_instructions in groupby(
        sorted(instructions, key=attrgetter("operation")),
        key=attrgetter("operation"),
    ):
        yield op, list(op_instructions)


def create_adding_message(threads: list[Thread]) -> str:
    return (
        f"{EMOJI_NAMESPACE} {EMOJI_ADD} Podle tvých zájmů jsem tě přidalo do těchto vláken:"
        f"\n\n{format_threads(threads)}\n\n"
        f"Jsou to „zájmové skupinky”. Sdílí se v nich "
        "novinky, drby, tipy, filozofické úvahy, vysvětlují obecnější koncepty, "
        "nebo řeší společné úlohy."
        "\n\n"
        "Pokud něco vyloženě debuguješ, je lepší tím skupinky nespamovat. "
        "Založ vlákno v poradně "
        f"https://discord.com/channels/{CLUB_GUILD_ID}/{ClubChannelID.QA} "
        "a do vhodné skupinky pak na něho dej pouze odkaz."
    )


def create_info_message(threads: list[Thread]) -> str:
    return (
        f"{EMOJI_NAMESPACE} {EMOJI_INFO} Podle tvých zájmů by tě mělo bavit sledování těchto vláken:"
        f"\n\n{format_threads(threads)}\n\n"
        f"Ale nejsi v nich! Pokud tě tyhle „zájmové skupinky” už nebavily a přes tlačítko "
        "_Sledující/Sledovat_ jsi z nich záměrně zmizel(a), je to v pořádku. "
        "Já už tě přidávat nebudu. "
        "Ale třeba to byl jen nějaký omyl, tak aspoň píšu."
        "\n\n"
        "Svoje zájmy můžeš upravovat v sekci **Kanály a role**, kterou najdeš úplně nahoře v seznamu kanálů."
    )


def format_threads(threads: list[Thread]) -> str:
    return "\n".join(
        f"**{thread.name}**\nOdkaz: {thread.jump_url}" for thread in threads
    )


def contains_adding_message(messages: list[ClubMessage], thread_url: str) -> bool:
    return contains_message(
        messages, f"{EMOJI_NAMESPACE} {EMOJI_ADD}", thread_url.rstrip("/")
    )


def contains_info_message(messages: list[ClubMessage], thread_url: str) -> bool:
    return contains_message(
        messages, f"{EMOJI_NAMESPACE} {EMOJI_INFO}", thread_url.rstrip("/")
    )


def contains_message(messages: list[ClubMessage], prefix: str, text: str) -> bool:
    for message in messages:
        if message.content.startswith(prefix) and text in message.content:
            return True
    return False
