import asyncio
import re
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
from juniorguru.models.base import db
from juniorguru.models.club import ClubDocumentedRole
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


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["roles"])
@click.option(
    "--path",
    "tips_path",
    default="juniorguru/data/tips",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
)
def main(tips_path):
    with db.connection_context():
        roles = {
            documented_role.slug: documented_role.id
            for documented_role in ClubDocumentedRole.listing()
        }
    tips = list(load_tips(tips_path, roles=roles))
    logger.info(f"Loaded {len(tips)} tips")
    discord_sync.run(sync_tips, tips)


def load_tips(tips_path: Path, roles=None):
    for tip_path in tips_path.glob("*.md"):
        if tip_path.name == "README.md":
            continue
        logger.info(f"Loading tip {tip_path}")
        yield {'url': get_tip_url(tip_path),
               **parse_tip(tip_path.read_text(), roles=roles)}


def get_tip_url(path: Path, cwd: Path=None) -> str:
    cwd = cwd or Path.cwd()
    path = path.absolute().relative_to(cwd)
    return f'https://github.com/honzajavorek/junior.guru/blob/main/{path}'


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

    return dict(emoji=emoji, title=title, content=markdown)


@db.connection_context()
@mutations.mutates_discord()
async def sync_tips(client: ClubClient, tips: list[dict]):
    channel = await client.fetch_channel(ClubChannelID.TIPS)
    threads = {get_starting_emoji(thread.name): thread for thread in channel.threads}
    await asyncio.gather(*[
        asyncio.create_task(
            update_tip(threads[tip["emoji"]], tip) if tip["emoji"] in threads else create_tip(channel, tip)
        )
        for tip in tips
    ])


async def create_tip(channel: ForumChannel, tip: dict) -> Thread:
    logger.info(f'Creating tip: {tip["title"]}')
    thread = await channel.create_thread(name=tip["title"],
                                         content=tip["content"],
                                         allowed_mentions=AllowedMentions.none(),
                                         auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION,
                                         view=(await create_view(tip['url'])))
    message = thread.get_partial_message(thread.id)
    await message.edit(suppress=True)
    await message.add_reaction('✅')
    return thread


async def update_tip(thread: Thread, tip: dict) -> None:
    logger.info(f'Updating tip: {tip["title"]}')
    message = (
        thread.starting_message
        if thread.starting_message
        else (await thread.fetch_message(thread.id))
    )
    view = await create_view(tip['url'])

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
    return ui.View(ui.Button(
            emoji="<:github:842685206095724554>",
            label="Navrhnout změny v textu",
            url=url,
        ))
