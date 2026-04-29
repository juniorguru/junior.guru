import asyncio
from datetime import date, timedelta
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlparse

import click
import requests
from discord import Colour, Embed, File, ForumChannel, ForumTag, Message, Thread, ui

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers, mutations
from jg.coop.lib.discord_club import ClubChannelID, ClubClient, parse_channel
from jg.coop.lib.discord_markdown import truncate_discord_markdown
from jg.coop.lib.mutations import MutationsNotAllowedError, mutating_discord
from jg.coop.lib.text import emoji_url, remove_emoji
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.job import DiscordJob, ListedJob


JOBS_REPEATING_PERIOD_DAYS = 30

MAX_FORUM_TAGS = 5

JOB_DESCRIPTION_MAX_LENGTH = 1500

IMAGES_DIR = Path("src/jg/coop/images")


class ForumTagName(StrEnum):
    ccpp = "C & C++"
    csharp = "C#"
    dataanalysis = "datová analýza"
    database = "databáze"
    hardware = "hardware"
    htmlcss = "HTML & CSS"
    javakotlin = "Java & Kotlin"
    javascript = "JavaScript"
    linux = "Linux"
    node = "Node.js"
    php = "PHP"
    python = "Python"
    ruby = "Ruby"
    swift = "Swift"
    testing = "testování"


TAGS_MAPPING = {
    "c": ForumTagName.ccpp,
    "cpp": ForumTagName.ccpp,
    "csharp": ForumTagName.csharp,
    "css": ForumTagName.htmlcss,
    "dataanalysis": ForumTagName.dataanalysis,
    "database": ForumTagName.database,
    "excel": ForumTagName.dataanalysis,
    "hardware": ForumTagName.hardware,
    "html": ForumTagName.htmlcss,
    "java": ForumTagName.javakotlin,
    "javascript": ForumTagName.javascript,
    "kotlin": ForumTagName.javakotlin,
    "linux": ForumTagName.linux,
    "node": ForumTagName.node,
    "pandas": ForumTagName.dataanalysis,
    "php": ForumTagName.php,
    "powerbi": ForumTagName.dataanalysis,
    "python": ForumTagName.python,
    "ruby": ForumTagName.ruby,
    "swift": ForumTagName.swift,
    "testing": ForumTagName.testing,
}


logger = loggers.from_path(__file__)


@cli.sync_command(
    dependencies=[
        "club-content",
        "jobs-logos",
        "jobs-locations",
        "jobs-tech-tags",
    ]
)
@click.option("--channel", "channel_id", default="jobs", type=parse_channel)
def main(channel_id: int):
    discord_task.run(sync_jobs, channel_id)


@db.connection_context()
async def sync_jobs(client: ClubClient, channel_id: int):
    channel = await client.club_guild.fetch_channel(channel_id)
    since_on = date.today() - timedelta(days=JOBS_REPEATING_PERIOD_DAYS)

    logger.debug("Checking if tags are in sync")
    tags_enum = set(map(str, ForumTagName))
    tags_discord = set(t.name for t in channel.available_tags)
    if tags_enum != tags_discord:
        raise ValueError(f"Tags don't match! {tags_discord ^ tags_enum}")

    logger.debug("Clearing database of Discord jobs")
    DiscordJob.drop_table()
    DiscordJob.create_table()

    logger.debug("Clearing Discord URLs")
    jobs = ListedJob.listing()
    for job in jobs:
        job.discord_url = None
        job.save()
    logger.info(f"Currently listed jobs: {len(jobs)}")

    messages = list(ClubMessage.forum_listing(channel_id))
    logger.info(f"Found {len(messages)} threads since {since_on}")
    for message in messages:
        if message.created_at.date() > since_on:
            thread: Thread = await client.fetch_channel(message.id)
            comments_count = len(ClubMessage.channel_listing(message.channel_id)) - 1
            if message.author_is_bot:
                if not message.ui_urls:
                    raise ValueError(f"No URL: {message.url}")
                if len(message.ui_urls) > 1:
                    raise ValueError(
                        f"Multiple URLs: {message.url} {message.ui_urls!r}"
                    )
                try:
                    url = message.ui_urls[0]
                    logger.debug(f"Looking up: {url}")
                    job = ListedJob.get_by_url(url)
                except ListedJob.DoesNotExist:
                    logger.info(f"Archiving: {url}")
                    await archive_thread(thread)
                else:
                    logger.info(f"Syncing: {url}")
                    job.discord_url = message.url
                    job.upvotes_count = message.upvotes_count
                    job.comments_count = comments_count
                    job.save()
                    await unarchive_thread(thread)
            else:
                logger.info(f"Creating manually submitted job: {message.url}")
                DiscordJob.create(
                    title=remove_emoji(message.channel_name),
                    author=message.author,
                    posted_on=message.created_at.date(),
                    description_discord=message.content,
                    url=message.url,
                    upvotes_count=message.upvotes_count,
                    comments_count=comments_count,
                )
                await unarchive_thread(thread)
    logger.info(f"Created {DiscordJob.count()} Discord jobs")

    logger.info("Ensuring there is an up-to-date summary post")
    summary_message = ClubMessage.forum_guide(channel_id)
    await ensure_summary(
        channel,
        summary_message.id if summary_message else None,
        "Aktuální ručně přidané inzeráty 👈 (aby nezapadly)",
        prepare_summary_content(DiscordJob.listing(), ListedJob.submitted_listing()),
    )

    jobs = ListedJob.no_discord_listing()
    logger.info(f"Posting {len(jobs)} new jobs to the channel")
    for job in jobs:
        logger.info(f"Posting: {job.url}")
        forum_tags = get_forum_tags(TAGS_MAPPING, channel.available_tags, job.tech_tags)
        if len(forum_tags) > MAX_FORUM_TAGS:
            raise ValueError(f"Too many tags: {[tag.name for tag in forum_tags]}")
        job.discord_url = await create_thread(channel, job, forum_tags)
        job.save()


def get_forum_tags(
    mapping: dict[str, ForumTagName],
    forum_tags: list[ForumTag],
    tech_tags: list[str],
    limit: int = MAX_FORUM_TAGS,
    dispensables: list[ForumTagName] | None = None,
) -> list[ForumTag]:
    forum_tag_names = set(map(str, filter(None, (mapping.get(tt) for tt in tech_tags))))
    forum_tags = [ft for ft in forum_tags if ft.name in forum_tag_names]

    dispensables = dispensables or []
    while len(forum_tags) > limit:
        if dispensables:
            dispensable = dispensables.pop()
            forum_tags = [ft for ft in forum_tags if ft.name != dispensable]
        else:
            forum_tags.pop()
    return forum_tags


@mutations.mutates_discord()
async def ensure_summary(
    channel: ForumChannel, summary_id: int | None, title: str, content: str
) -> None:
    if summary_id:
        thread = channel.get_thread(summary_id)
    else:
        thread = await channel.create_thread(name=title, content=content)

    params = {}
    if summary_id and thread.name != title:
        params["name"] = title
    if not thread.is_pinned():
        params["pinned"] = True
    if not thread.locked:
        params["locked"] = True
    if params:
        await thread.edit(**params)

    if summary_id:
        message = await thread.fetch_message(thread.id)
        params = {}
        if message.content != content:
            params["content"] = content
        if params:
            await message.edit(**params)


def prepare_summary_content(
    manual_jobs: list[DiscordJob], submitted_jobs: list[ListedJob]
) -> str:
    text = (
        "Pokud víš o zajímavé nabídce pro juniory, "
        f"**přidej ji normálně ručně** do <#{ClubChannelID.JOBS}> jako nový příspěvek. "
        "Hned jak si jí všimnu, odkážu ji automaticky i tady. "
    )
    if manual_jobs:
        items = [f"- [{job.title}]({job.url})" for job in manual_jobs]
        text += "\n\n## Aktuální inzeráty od členů ❤️\n\n"
        text += "\n".join(items)
    if submitted_jobs:
        items = [f"- [{job.title}]({job.discord_url})" for job in submitted_jobs]
        text += "\n\n## Aktuální inzeráty z junior.guru 💛\n\n"
        text += "\n".join(items)
    text += (
        "\n\n## Inzeráty odjinud ✨\n\n"
        f"Už žádné „požadujeme 4 roky zkušeností“. Každý den do <#{ClubChannelID.JOBS}> "
        "stahuju inzeráty z různých zdrojů a pomocí umělé inteligence vybírám jen ty "
        "vhodné pro začátečníky.\n\n"
        "Tytéž inzeráty najdeš i na [junior.guru/jobs](https://junior.guru/jobs/), ale tady "
        "se o nich dovíš hned, a navíc na ně můžeš reagovat a komentovat pod nimi."
    )
    return text


@mutations.mutates_discord()
async def archive_thread(thread: Thread) -> None:
    await thread.archive()


@mutations.mutates_discord()
async def unarchive_thread(thread: Thread) -> None:
    if not thread.archived:
        return
    await thread.unarchive()


async def create_thread(
    channel: ForumChannel,
    job: ListedJob,
    forum_tags: list[ForumTag],
    sleep_on_retry: int = 3,
) -> str:
    try:
        with mutating_discord(channel, raises=True) as proxy:
            for attempt_no in range(1, 4):
                logger.debug(f"Creating thread, attempt #{attempt_no}")
                thread: Thread = await proxy.create_thread(
                    applied_tags=forum_tags,
                    **(await prepare_thread_params(job)),
                )

                logger.debug("Verifying that images got uploaded correctly")
                message: Message = await thread.fetch_message(thread.id)
                if message.attachments:
                    logo_url = message.attachments[0].url
                    response = requests.head(logo_url)
                    logo_bytes_count = int(response.headers.get("Content-Length", 0))
                else:
                    logo_url = None
                    logo_bytes_count = 1

                if logo_bytes_count == 0:
                    logger.warning(
                        f"Logo attachment is empty (attempt #{attempt_no}): {logo_url}"
                        f" ({thread.name}: {thread.jump_url})"
                    )
                    await thread.delete()
                    await asyncio.sleep(sleep_on_retry)
                else:
                    return thread.jump_url
        logger.error("Failed to create thread!")
        return None
    except MutationsNotAllowedError:
        return None


def get_company_web_name(company_url: str) -> str:
    parsed_url = urlparse(company_url)
    return parsed_url.netloc.replace("www.", "") or company_url


async def prepare_thread_params(job: ListedJob) -> dict:
    content = f"{job.location_text or '?'} — {job.company_name}"
    if job.tech_tags:
        content += " ".join(f"`#{tag}`" for tag in sorted(job.tech_tags))
    content += f"-# Zdroj: {', '.join(job.sources)}"
    content += "\n\n"

    files = []
    embeds = []
    logo_attachment_url = None
    if job.company_logo_path:
        files.append(File(IMAGES_DIR.absolute() / job.company_logo_path))
        logo_attachment_url = f"attachment://{Path(job.company_logo_path).name}"

    description = truncate_discord_markdown(
        job.description_discord,
        max_length=JOB_DESCRIPTION_MAX_LENGTH,
        placeholder="…",
    )
    if description != job.description_discord:
        description += "\n\n-# (zkráceno, pro celý inzerát klikni na tlačítko dole)"

    # job
    job_embed = Embed(title=job.title, url=job.url, description=description)
    author_params = {"name": job.company_name}
    if job.company_url:
        author_params["url"] = job.company_url
    if logo_attachment_url:
        author_params["icon_url"] = logo_attachment_url
    job_embed.set_author(**author_params)
    job_embed.set_footer(text="Inzerát z junior.guru")
    embeds.append(job_embed)

    # company
    company_embed = Embed(title=job.company_name, description="", colour=Colour.blue())
    if logo_attachment_url:
        company_embed.set_image(url=logo_attachment_url)
    if job.company_url:
        web_name = get_company_web_name(job.company_url)
        company_embed.add_field(
            name="web",
            value=f"[{web_name}]({job.company_url})",
            inline=False,
        )
    if job.company_linkedin_url:
        company_embed.add_field(
            name="LinkedIn",
            value=f"[Hledat „{job.company_name}“]({job.company_linkedin_url})",
            inline=False,
        )
    if job.company_atmoskop_url:
        company_embed.add_field(
            name="Atmoskop",
            value=f"[Hledat „{job.company_name}“]({job.company_atmoskop_url})",
            inline=False,
        )
    if job.company_jakybylpohovor_url:
        company_embed.add_field(
            name="Jaký byl pohovor?",
            value=f"[Hledat „{job.company_name}“]({job.company_jakybylpohovor_url})",
            inline=False,
        )
    if job.company_search_url:
        company_embed.add_field(
            name="Google",
            value=f"[Hledat „{job.company_name}“]({job.company_search_url})",
            inline=False,
        )
    embeds.append(company_embed)

    # reason
    if job.reason:
        reason_embed = Embed(description=f"_{job.reason}_")
        reason_embed.set_author(
            name="Proč si můj AI mozeček myslí, že je to juniorní",
            icon_url=emoji_url("✨"),
        )
        embeds.append(reason_embed)

    return dict(
        name=job.title_short,
        content=content,
        files=files,
        embeds=embeds,
        view=ui.View(ui.Button(emoji="👉", label="Celý inzerát", url=job.url)),
    )
