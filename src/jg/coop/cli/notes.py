import asyncio
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import click
import discord

from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.discord_club import (
    ClubClient,
    ClubMemberID,
    emoji_name,
    get_or_create_dm_channel,
    get_pinned_message_url,
    get_reaction,
    parse_discord_link,
)


EMOJI_RE = re.compile(r"^emoji:\s*(\S.*?)\s*$", re.MULTILINE)

NOTES_END = "\n\n#} -->"


logger = loggers.from_path(__file__)


@click.command()
@click.option(
    "--handbook-dir",
    default=Path("src/jg/coop/web/docs/handbook"),
    type=click.Path(path_type=Path, exists=True, file_okay=False),
)
@click.option("--check-emoji", default="✅")
@click.pass_context
def main(context: click.Context, handbook_dir: Path, check_emoji: str) -> None:
    mutations.allow("discord")
    context.call_on_close(mutations.allow_none)
    discord_task.run(process_pins, handbook_dir, check_emoji)


async def process_pins(
    client: ClubClient, handbook_dir: Path, check_emoji: str
) -> None:
    emoji_mapping = get_handbook_emoji_mapping(handbook_dir.glob("*.md"))
    notes_mapping = defaultdict(list)

    dm_channel = await get_or_create_dm_channel(client.get_user(ClubMemberID.HONZA))
    count = 0
    async for message in dm_channel.history(limit=None):
        count += 1
        if not message.reactions:
            logger.debug(f"Skipping {message.jump_url}")
            continue
        if get_reaction(message.reactions, check_emoji):
            logger.debug(f"Already processed {message.jump_url}")
            continue
        logger.info(f"Processing {message.jump_url}")
        for reaction in message.reactions:
            emoji = emoji_name(reaction.emoji)
            try:
                path = emoji_mapping[emoji]
            except KeyError:
                raise KeyError(
                    f"Unknown emoji {emoji} in reactions to {message.jump_url} (known: {list(emoji_mapping)!r})"
                )
            notes_mapping[path].append(message)
    logger.info(
        f"Done processing {count} messages, collected notes for {len(notes_mapping)} pages"
    )

    for path, messages in notes_mapping.items():
        text = path.read_text()
        logger.info(f"Adding {len(messages)} notes to {path}")
        notes = []
        for message in messages:
            link_ids = parse_discord_link(get_pinned_message_url(message))
            try:
                channel = await client.club_guild.fetch_channel(link_ids["channel_id"])
            except discord.errors.NotFound:
                logger.warning(
                    f"Channel #{link_ids['channel_id']} not found, {message.jump_url}"
                )
            else:
                pinned_message = await channel.fetch_message(link_ids["message_id"])
                note = f"--- {pinned_message.jump_url}\n{pinned_message.content}\n---\n"
                notes.append(note)
        notes_text = "\n\n" + "\n\n".join(notes) + NOTES_END
        path.write_text(text.replace(NOTES_END, notes_text))
        await asyncio.gather(
            *[message.add_reaction(check_emoji) for message in messages]
        )


def get_handbook_emoji_mapping(handbook_paths: Iterable[Path]) -> dict[str, Path]:
    mapping = {}
    for path in sorted(handbook_paths):
        emoji = parse_emoji(path.read_text())
        if emoji in mapping:
            raise ValueError(
                f"Emoji {emoji} is duplicated in {path} and {mapping[emoji]}"
            )
        mapping[emoji] = path.absolute()
    return mapping


def parse_emoji(source: str) -> str:
    if not (match := EMOJI_RE.search(source)):
        raise ValueError("Missing 'emoji: ...' line")

    return match.group(1)
