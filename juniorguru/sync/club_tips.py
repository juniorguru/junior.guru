import asyncio
import re
from datetime import date
from pathlib import Path

import click
from discord import AllowedMentions, ForumChannel, Thread, ui

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers, mutations
from juniorguru.lib.discord_club import (
    ClubChannelID,
    ClubClient,
    ClubMemberID,
    get_starting_emoji,
    parse_channel,
)
from juniorguru.lib.reading_time import reading_time
from juniorguru.lib.remove_emoji import remove_emoji
from juniorguru.models.base import db
from juniorguru.models.club import ClubDocumentedRole, ClubMessage
from juniorguru.sync.club_threads import DEFAULT_AUTO_ARCHIVE_DURATION


REFERENCE_RE = re.compile(
    r"""
    <
        (?P<prefix>[#@&]+)
        (?P<value>[^>]+)
    >
""",
    re.VERBOSE,
)

DOSE_EMOJI = "💡"

DEFAULT_REACTION_EMOJI = "✅"


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["roles", "club-content"])
@click.option(
    "--path",
    "tips_path",
    default="juniorguru/data/tips",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
)
@click.option("--force-dose", is_flag=True)
def main(tips_path: Path, force_dose: bool):
    with db.connection_context():
        roles = {
            documented_role.slug: documented_role.id
            for documented_role in ClubDocumentedRole.listing()
        }
    tips = list(load_tips(tips_path, roles=roles))
    logger.info(f"Loaded {len(tips)} tips")
    discord_sync.run(sync_tips, tips)
    discord_sync.run(dose_tips, tips, force_dose)


def load_tips(tips_path: Path, roles=None):
    for tip_path in sorted(tips_path.glob("*.md")):
        if tip_path.name == "README.md":
            continue
        logger.info(f"Loading tip {tip_path}")
        yield dict(
            url=get_tip_url(tip_path), **parse_tip(tip_path.read_text(), roles=roles)
        )


def get_tip_url(path: Path, cwd: Path = None) -> str:
    cwd = cwd or Path.cwd()
    path = path.absolute().relative_to(cwd)
    return f"https://github.com/honzajavorek/junior.guru/blob/main/{path}"


def parse_tip(markdown: str, roles=None) -> dict:
    markdown = markdown.strip()
    roles = {slug.upper(): id for slug, id in (roles or {}).items()}

    try:
        title_match = re.search(r"^# (.+)\n", markdown)
        title = title_match.group(1).strip()
        markdown = markdown[title_match.end() :].strip()
    except Exception as e:
        raise ValueError("Could not parse title") from e

    emoji = get_starting_emoji(title)
    if not emoji:
        raise ValueError(f"Could not parse emoji: {title!r}")

    markdown = re.sub(r"\n+## ", "\n## ", markdown)
    resolvers = {
        "@&": lambda value: roles[value],
        "@": lambda value: ClubMemberID[value],
        "#": parse_channel,
    }

    def resolve_reference(match: re.Match) -> str:
        prefix = match.group("prefix")
        value = match.group("value")
        try:
            return f"<{prefix}{resolvers[prefix](value)}>"
        except Exception as e:
            raise ValueError(f"Could not parse reference: {prefix}{value!r}") from e

    markdown = REFERENCE_RE.sub(resolve_reference, markdown)

    try:
        lead = markdown.split("\n", 1)[0]
    except Exception as e:
        raise ValueError("Could not parse lead") from e

    return dict(emoji=emoji, title=title, lead=lead, content=markdown)


@db.connection_context()
@mutations.mutates_discord()
async def sync_tips(client: ClubClient, tips: list[dict]):
    channel = await client.fetch_channel(ClubChannelID.TIPS)
    threads = threads_by_emoji(channel.threads)
    await asyncio.gather(
        *[
            asyncio.create_task(
                update_tip(threads[tip["emoji"]], tip)
                if tip["emoji"] in threads
                else create_tip(channel, tip)
            )
            for tip in tips
        ]
    )


async def create_tip(channel: ForumChannel, tip: dict) -> Thread:
    logger.info(f'Creating tip: {tip["title"]}')
    thread = await channel.create_thread(
        name=tip["title"],
        content=tip["content"],
        allowed_mentions=AllowedMentions.none(),
        auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION,
        view=(await create_view(tip["url"])),
    )
    message = thread.get_partial_message(thread.id)
    await message.edit(suppress=True)
    await message.add_reaction(DEFAULT_REACTION_EMOJI)
    return thread


async def update_tip(thread: Thread, tip: dict) -> None:
    logger.info(f'Updating tip: {tip["title"]}')
    message = (
        thread.starting_message
        if thread.starting_message
        else (await thread.fetch_message(thread.id))
    )
    view = await create_view(tip["url"])

    thread_params = {}
    if thread.archived:
        thread_params["archived"] = False
    if thread.auto_archive_duration != DEFAULT_AUTO_ARCHIVE_DURATION:
        thread_params["auto_archive_duration"] = DEFAULT_AUTO_ARCHIVE_DURATION
    if thread.name != tip["title"]:
        thread_params["name"] = tip["title"]
    if thread_params:
        logger.debug("Updating thread")
        await thread.edit(**thread_params)

    message_params = {}
    if message.content != tip["content"]:
        message_params["content"] = tip["content"]
        message_params["suppress"] = True
        message_params["allowed_mentions"] = AllowedMentions.none()
    try:
        button = message.components[0].children[0]
        if button.url != view.children[0].url:
            raise ValueError("URL mismatch")
        if button.label != view.children[0].label:
            raise ValueError("Label mismatch")
    except (IndexError, AttributeError, ValueError):
        message_params["view"] = view
    if message_params:
        logger.debug("Updating message")
        await message.edit(**message_params)


async def create_view(url: str) -> ui.View:  # View's __init__ touches the event loop
    return ui.View(
        ui.Button(
            emoji="<:github:842685206095724554>",
            label="Navrhnout změny v textu",
            url=url,
        )
    )


@db.connection_context()
async def dose_tips(client: ClubClient, tips: list[dict], force_dose: bool):
    channel_tips = await client.fetch_channel(ClubChannelID.TIPS)
    threads = threads_by_emoji(channel_tips.threads)

    channel = await client.fetch_channel(ClubChannelID.NEWCOMERS)
    last_dose_db_message = ClubMessage.last_bot_message(
        ClubChannelID.NEWCOMERS, DOSE_EMOJI
    )

    if last_dose_db_message:
        if last_dose_db_message.created_at.date() == date.today():
            logger.info("Already dosed today")
            if force_dose:
                logger.warning("Forcing dose!")
            else:
                return
        logger.info("Figuring out what to dose")
        last_dose_message = await channel.fetch_message(last_dose_db_message.id)
        last_dose_button = last_dose_message.components[0].children[0]
        dose_index = 0
        for index, tip in enumerate(tips):
            thread = threads[tip["emoji"]]
            if last_dose_button.url == thread.jump_url:
                logger.info(f"Previous dose: {tip['title']}, {thread.jump_url}")
                dose_index = index + 1
                break
        dose_tip = (tips + tips)[dose_index]
    else:
        logger.info("No previous dose found")
        dose_tip = tips[0]
    dose_thread = threads[dose_tip["emoji"]]

    logger.info(f"Dosing: {dose_tip['title']} - {dose_thread.jump_url}")
    newcomers_mention = ClubDocumentedRole.get_by_slug("newcomer").mention
    content = f"{DOSE_EMOJI} **Tip dne** pro {newcomers_mention} ({reading_time(len(dose_tip['content']))} min čtení)"
    with mutations.mutating_discord(channel) as proxy:
        await proxy.send(
            content,
            allowed_mentions=AllowedMentions(users=False, roles=True),
            view=ui.View(
                ui.Button(
                    emoji=dose_tip["emoji"],
                    label=remove_emoji(dose_tip["title"]),
                    url=dose_thread.jump_url,
                )
            ),
        )


def threads_by_emoji(threads: list[Thread]) -> dict[str, Thread]:
    return {get_starting_emoji(thread.name): thread for thread in threads}
