import tempfile
from datetime import date
from operator import attrgetter

import click
import httpx2
from discord import Embed, File, MessageType
from emoji import emojize, is_emoji

from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.discord_club import ClubClient, parse_channel
from jg.coop.lib.text import emoji_url


logger = loggers.from_path(__file__)


@click.command()
@click.argument("src_channel_id", type=parse_channel)
@click.argument("dst_forum_id", type=parse_channel)
@click.option(
    "--archive-id",
    type=int,
    default=878944218545025034,
    help="Category ID to move the archived channel to",
)
@click.option(
    "-t",
    "--tag",
    type=str,
    default="zájmová skupinka",
    help="Forum tag to set on the thread",
)
@click.option(
    "-n", "--name", type=str, default=None, prompt=True, help="New thread name"
)
@click.option(
    "-d",
    "--description",
    type=str,
    default=None,
    prompt=True,
    help="New thread description",
)
@click.option("-l", "--limit", type=int, default=5, help="How many messages to move")
@click.option(
    "-r",
    "--role",
    "role_id",
    type=int,
    default=None,
    help="Role ID to mention in the thread",
)
def main(
    src_channel_id: int,
    dst_forum_id: int,
    archive_id: int,
    tag: str,
    name: str,
    description: str,
    limit: int,
    role_id: int | None,
):
    mutations.allow("discord")
    discord_task.run(
        move,
        src_channel_id,
        dst_forum_id,
        archive_id,
        tag,
        name,
        description,
        limit,
        role_id,
    )


async def move(
    client: ClubClient,
    src_channel_id: int,
    dst_forum_id: int,
    archive_id: int,
    tag: str,
    name: str,
    description: str,
    limit: int,
    role_id: int | None,
):
    src_channel = await client.club_guild.fetch_channel(src_channel_id)

    emoji = emojize(src_channel.topic, language="alias").split()[-1]
    if not is_emoji(emoji):
        raise ValueError(
            f"Channel topic must end with an emoji, got: {src_channel.topic!r}"
        )

    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        response = httpx2.get(emoji_url(emoji))
        response.raise_for_status()
        f.write(response.content)
        f.flush()

        logger.info(
            f"Creating thread in forum #{dst_forum_id} with name {name!r} and emoji {emoji!r}"
        )
        dst_forum = await client.club_guild.fetch_channel(dst_forum_id)
        thread = await dst_forum.create_thread(
            name=name,
            content=description,
            applied_tags=[
                forum_tag
                for forum_tag in dst_forum.available_tags
                if forum_tag.name == tag
            ],
            file=File(f.name, filename=f"{src_channel.id}-emoji.png"),
        )
    today = date.today()
    await thread.send(
        f"ℹ️ Původně jsme na tohle téma měli kanál **#{src_channel.name}**, ale "
        f"Honza se pak rozhodl, že takové kanály už mít samostatně nebudeme. "
        f"Takže {today:%-d.%-m.%Y} jsem z něj udělalo tuhle zájmovou skupinku. "
        f"Původní kanál je archivovaný tady: <#{src_channel.id}> "
    )
    logger.info(f"Thread created: {thread.jump_url}")

    logger.info(f"Forwarding {limit} last messages")
    messages = sorted(
        [
            message
            async for message in src_channel.history(limit=limit, oldest_first=False)
        ],
        key=attrgetter("id"),
    )
    if messages:
        await thread.send(
            f"Aby se úplně neztratil kontext, hodím sem teď aspoň posledních {limit} zpráv z původního kanálu…"
        )
    for message in messages:
        if message.type in [MessageType.default, MessageType.reply]:
            logger.debug(f"Moving message {message.id} to thread {thread.id}")
            embed = Embed()
            embed.set_author(
                name=str(message.author), icon_url=message.author.display_avatar.url
            )
            await thread.send(embed=embed)
            await message.forward_to(thread)
        else:
            logger.warning(f"Skipping message {message.id} of type {message.type}")

    if role_id:
        logger.info("Mentioning role")
        await thread.send(
            f"<@&{role_id}> Tady máte svůj nový domov! Hezky si to tu zabydlete <:meowsheart:1002448596572061746>"
        )

    logger.info(f"Archiving source channel #{src_channel.name}")
    await src_channel.send(
        "🔒 Tento kanál končí a putuje do archivu, kde zůstane ke čtení a prohledávání. "
        "Honza dělá změny v tom, jak v klubu fungují zájmy o jednotlivé technologie nebo oblasti IT. "
        "Místo samostatných kanálů teď budou „zájmové skupinky”, "
        "které může každý nejen podle svých preferencí sledovat, ale také vytvářet! "
        "Na téma totoho kanálu jsem ti už ale skupinku právě teď založilo. "
        f"Párty pokračuje tady: <#{thread.id}> <a:meowparty:851385606571163688>"
    )
    archive_category = await client.club_guild.fetch_channel(archive_id)
    await src_channel.edit(
        name=f"archiv-{src_channel.name}",
        category=archive_category,
        sync_permissions=True,
    )
