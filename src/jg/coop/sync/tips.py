import asyncio
import re
from datetime import date, timedelta
from operator import attrgetter
from pathlib import Path

import click
from discord import AllowedMentions, ForumChannel, NotFound, Thread, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.discord_club import (
    DEFAULT_AUTO_ARCHIVE_DURATION,
    ClubChannelID,
    ClubClient,
    ClubMemberID,
    fetch_threads,
    get_starting_emoji,
    is_message_over_period_ago,
    resolve_references,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.lib.reading_time import reading_time
from jg.coop.lib.text import remove_emoji
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.role import DocumentedRole
from jg.coop.models.tip import Tip


CONTROL_EMOJI = "💡"

DEFAULT_REACTION_EMOJI = "✅"

# TODO
# - create separate reminders.py and reminders.yml
# - the periodicity of reminders should be just days, integer
# - if multiple reminders with the same periodicity go to the same channel, they should be rotated by random
# - maybe its just newcomers, intro, and then we should dose tips to chat monthly?!?
REMINDERS = [
    (
        "👋",
        ClubChannelID.NEWCOMERS,
        (
            "Ahoj! Toto je speciální kanál, který vidí jen **nově příchozí** jako ty a **moderátoři**. "
            "Pokud není jasné, jak něco funguje, neboj se tady zeptat. "
            "Rádi poradíme, nasměrujeme. Žádná otázka není blbá.\n\n"
            "Každý den sem posílám jeden tip, který by měl pomoci s orientací v klubu. "
            f"Všechny najdeš tady: <#{ClubChannelID.TIPS}>"
        ),
        timedelta(days=7),
    ),
    (
        CONTROL_EMOJI,
        ClubChannelID.INTRO,
        "Proč je dobré se představit ostatním a co vůbec napsat? Přečti si klubový tip {👋}",
        timedelta(days=30),
    ),
    # (
    #     CONTROL_EMOJI,
    #     ClubChannelID.CHAT,
    #     "Chceš se družit a potkávat s lidmi v místě, kde žiješ? Přečti si klubový tip {👭}",
    #     timedelta(days=30),
    # ),
]


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["roles", "club-content"])
@click.option(
    "--path",
    "tips_path",
    default="src/jg/coop/data/tips",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
)
@click.option("--force-dose", is_flag=True)
@click.option("--force-reminders", is_flag=True)
def main(tips_path: Path, force_dose: bool, force_reminders: bool):
    with db.connection_context():
        roles = {
            documented_role.slug: documented_role.club_id
            for documented_role in DocumentedRole.listing()
        }
    tips = list(load_tips(tips_path, roles=roles))
    logger.info(f"Loaded {len(tips)} tips")
    discord_task.run(sync_tips, tips)
    discord_task.run(dose_tips, tips, force_dose)
    discord_task.run(ensure_reminders, REMINDERS, force_reminders)


def load_tips(tips_path: Path, roles: dict[str, int] | None = None):
    for tip_path in sorted(tips_path.glob("*.md")):
        if tip_path.name == "README.md":
            continue
        logger.info(f"Loading tip {tip_path}")
        position, slug = tip_path.stem.split("_", 1)
        yield dict(
            slug=slug,
            position=position,
            edit_url=get_edit_url(tip_path),
            **parse_tip(tip_path.read_text(), roles=roles),
        )


def get_edit_url(path: Path, cwd: Path = None) -> str:
    cwd = cwd or Path.cwd()
    path = path.absolute().relative_to(cwd)
    return f"https://github.com/juniorguru/junior.guru/blob/main/{path}"


def parse_tip(markdown: str, roles: dict[str, int] | None = None) -> dict:
    markdown = markdown.strip()

    try:
        title_match = re.search(r"^# (.+)\n", markdown)
        title = title_match.group(1).strip()
        markdown = markdown[title_match.end() :].strip()
    except Exception as e:
        raise ValueError("Could not parse title") from e

    emoji = get_starting_emoji(title)
    if not emoji:
        raise ValueError(f"Could not parse emoji: {title!r}")

    markdown = resolve_references(markdown, roles=roles)

    try:
        lead = markdown.split("\n", 1)[0]
    except Exception as e:
        raise ValueError("Could not parse lead") from e

    return dict(emoji=emoji, title=title, lead=lead, content=markdown)


@db.connection_context()
async def sync_tips(client: ClubClient, tips: list[dict]):
    logger.info("Syncing tips")
    tips_by_emoji = {tip["emoji"]: tip for tip in tips}
    tasks = []
    seen_emojis = set()
    channel = await client.fetch_channel(ClubChannelID.TIPS)
    threads = sorted(
        [
            thread
            async for thread in fetch_threads(channel)
            if thread.owner.id == ClubMemberID.BOT
        ],
        key=attrgetter("created_at"),
    )
    for thread in threads:
        emoji = get_starting_emoji(thread.name)
        if emoji in seen_emojis:  # duplicate
            tasks.append(asyncio.create_task(delete_thread(thread)))
        elif emoji in tips_by_emoji:  # update
            tip = tips_by_emoji[emoji]
            tasks.append(asyncio.create_task(update_tip(thread, tip)))
            seen_emojis.add(emoji)
        else:  # unknown, possibly old
            tasks.append(asyncio.create_task(delete_thread(thread)))
    for tip in tips:
        if tip["emoji"] not in seen_emojis:
            tasks.append(asyncio.create_task(create_tip(channel, tip)))
    await asyncio.gather(*tasks)

    Tip.drop_table()
    Tip.create_table()
    channel = await client.fetch_channel(ClubChannelID.TIPS)  # avoid cached data
    for emoji, thread in threads_by_emoji(channel.threads).items():
        data = tips_by_emoji[emoji]
        Tip.create(
            title_text=remove_emoji(data["title"]),
            discord_url=thread.jump_url,
            **data,
        )


@mutations.mutates_discord()
async def delete_thread(thread: Thread) -> None:
    logger.info(f"Deleting tip from {thread.created_at.date()}: {thread.name}")
    await thread.delete()


@mutations.mutates_discord()
async def create_tip(channel: ForumChannel, tip: dict) -> Thread:
    logger.info(f"Creating tip: {tip['title']}")
    thread = await channel.create_thread(
        name=tip["title"],
        content=tip["content"],
        allowed_mentions=AllowedMentions.none(),
        auto_archive_duration=DEFAULT_AUTO_ARCHIVE_DURATION,
        view=(await create_view(tip["edit_url"])),
    )
    message = thread.get_partial_message(thread.id)
    await message.edit(suppress=True)
    await message.add_reaction(DEFAULT_REACTION_EMOJI)


@mutations.mutates_discord()
async def update_tip(thread: Thread, tip: dict) -> None:
    logger.info(f"Updating tip: {tip['title']}")
    message = (
        thread.starting_message
        if thread.starting_message
        else (await thread.fetch_message(thread.id))
    )
    view = await create_view(tip["edit_url"])

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


# async, because View's __init__ touches the event loop 🙄
async def create_view(edit_url: str) -> ui.View:
    return ui.View(
        ui.Button(
            emoji="<:github:842685206095724554>",
            label="Upravit tip",
            url=edit_url,
        )
    )


@db.connection_context()
async def dose_tips(client: ClubClient, tips: list[dict], force: bool):
    logger.info("Dosing tips")
    channel_tips = await client.fetch_channel(ClubChannelID.TIPS)
    threads = threads_by_emoji(channel_tips.threads)

    channel = await client.fetch_channel(ClubChannelID.NEWCOMERS)
    last_dose_db_message = ClubMessage.last_bot_message(
        ClubChannelID.NEWCOMERS, CONTROL_EMOJI
    )

    if last_dose_db_message:
        if last_dose_db_message.created_at.date() == date.today():
            logger.info("Already dosed today")
            if force:
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
    newcomers_mention = DocumentedRole.get_by_slug("newcomer").mention
    content = f"{CONTROL_EMOJI} **Tip dne** pro {newcomers_mention} ({reading_time(len(dose_tip['content']))} min čtení)"
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


@db.connection_context()
async def ensure_reminders(
    client: ClubClient,
    reminders: list[tuple[str, ClubChannelID, str, timedelta]],
    force: bool,
):
    logger.info("Ensuring reminders")
    channel_tips = await client.fetch_channel(ClubChannelID.TIPS)
    tip_urls_by_emoji = {
        emoji: thread.jump_url
        for emoji, thread in threads_by_emoji(channel_tips.threads).items()
    }
    for control_emoji, channel_id, content_template, period in reminders:
        last_message = ClubMessage.last_bot_message(channel_id, control_emoji)
        if force:
            logger.warning("Forcing reminder!")
        elif is_message_over_period_ago(last_message, period):
            logger.warning(f"Last reminder is more than {period.days} old!")
        else:
            logger.info("Reminder is still fresh, skipping")
            return
        channel = await client.fetch_channel(channel_id)
        content = f"{control_emoji} {content_template.format(**tip_urls_by_emoji)}"
        logger.info(f"Sending: {content!r}")
        with mutating_discord(channel) as proxy:
            await proxy.send(content)
        if last_message:
            logger.info(f"Deleting previous reminder: {last_message.url}")
            try:
                message = await channel.fetch_message(last_message.id)
                with mutating_discord(message) as proxy:
                    await proxy.delete()
            except NotFound:
                logger.warning("Reminder not found, probably already deleted")


def threads_by_emoji(threads: list[Thread]) -> dict[str, Thread]:
    return {get_starting_emoji(thread.name): thread for thread in threads}
