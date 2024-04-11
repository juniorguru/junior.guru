from pathlib import Path

from discord import ButtonStyle, Color, Embed, NotFound, ui
from strictyaml import Bool, Int, Map, Optional, Seq, Str, Url, load

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubChannelID, ClubClient
from jg.coop.lib.mutations import MutationsNotAllowedError, mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.mentor import Mentor


MENTOR_EMOJI = "💁"

INFO_EMOJI = "💡"

DATA_PATH = Path("jg/coop/data/mentors.yml")

SCHEMA = Seq(
    Map(
        {
            "id": Int(),
            "name": Str(),
            Optional("company"): Str(),
            Optional("bio_url"): Url(),
            "topics": Str(),
            Optional("english_only", default=False): Bool(),
            Optional("book_url"): Url(),
        }
    )
)


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content"])
def main():
    discord_task.run(sync_mentoring)


@db.connection_context()
async def sync_mentoring(client: ClubClient):
    logger.info("Setting up db table")
    Mentor.drop_table()
    Mentor.create_table()

    logger.info("Parsing YAML")
    for yaml_record in load(DATA_PATH.read_text(), SCHEMA):
        Mentor.create(user=yaml_record.data["id"], **yaml_record.data)
    mentors = Mentor.listing()
    logger.debug(f"Loaded {len(mentors)} mentors from YAML")

    messages_trash = set(ClubMessage.channel_listing(ClubChannelID.MENTORING))
    info_message = ClubMessage.last_bot_message(ClubChannelID.MENTORING, INFO_EMOJI)
    discord_channel = await client.fetch_channel(ClubChannelID.MENTORING)

    return  # FIXME TODO https://app.circleci.com/pipelines/github/juniorguru/junior.guru/10230/workflows/877b3680-5b19-4586-ba74-10fc3b672b77/jobs/49075

    logger.info("Syncing mentors")
    for mentor in mentors:
        try:
            discord_member = await client.club_guild.fetch_member(mentor.user.id)
        except NotFound:
            logger.error(
                f"Not a member! #{mentor.id} ({mentor.name} from {mentor.company})"
            )
            continue
        mentor_params = get_mentor_params(
            mentor, thumbnail_url=discord_member.display_avatar.url
        )

        message = ClubMessage.last_bot_message(
            ClubChannelID.MENTORING, MENTOR_EMOJI, mentor.user.mention
        )
        if message:
            messages_trash.remove(message)
            logger.info(f"Editing existing message for mentor {mentor.name}")
            discord_message = await discord_channel.fetch_message(message.id)
            with mutating_discord(discord_message) as proxy:
                await proxy.edit(**mentor_params)
            mentor.message_url = message.url
            mentor.save()
        else:
            logger.info(f"Creating a new message for mentor {mentor.name}")
            if info_message:
                logger.info("Deleting info message")
                messages_trash.remove(info_message)
                info_discord_message = await discord_channel.fetch_message(
                    info_message.id
                )
                with mutating_discord(info_discord_message) as proxy:
                    await proxy.delete()
                info_message.delete_instance()
                info_message = None
            try:
                with mutating_discord(discord_channel, raises=True) as proxy:
                    discord_message = await proxy.send(**mentor_params)
            except MutationsNotAllowedError:
                pass
            else:
                mentor.message_url = discord_message.jump_url
                mentor.save()

    logger.info("Syncing info")
    info_content = f"{INFO_EMOJI} Co to tady je? Jak to funguje?"
    info_mentee_description = (
        "Pomohlo by ti pravidelně si s někým na hodinku zavolat a probrat svůj postup? "
        "Předchozí zprávy v tomto kanálu představují seznam **mentorů**, kteří se k takové pomoci nabídli. "
        "Postupuj následovně:\n"
        "\n"
        "1️⃣ 🧭 Stanov si dlouhodobější cíl (např. porozumět API)\n"
        "2️⃣ 👋 Podle tématu si vyber mentorku/mentora a rezervuj si čas na videohovor\n"
        "3️⃣ 🤝 Domluvte se, jak často si budete volat (např. každé dva týdny, půl roku)\n"
        "4️⃣ 📝 Rezervuj jednotlivé schůzky a předem měj jasno, co na nich chceš řešit\n"
        "5️⃣ 🚀 Mentor ti pomáhá dosáhnout cíle. Radí a posouvá tě správným směrem\n"
        "\n"
        "❤️ Mentoři jsou dobrovolníci, ne placení učitelé. Aktivita je na tvé straně. Važ si jejich času a dopřej jim dobrý pocit, pokud pomohli.\n"
    )
    info_mentor_description = (
        "🦸 I ty můžeš mentorovat! "
        "Nemusíš mít 10 let zkušeností v oboru. "
        "Pusť si [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski, ať víš, co od toho čekat. "
        "Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md). "
        "Potom napiš Honzovi, přidá tě do [seznamu](https://github.com/juniorguru/junior.guru/blob/main/jg/coop/data/mentors.yml)."
    )
    info_params = dict(
        content=info_content,
        embeds=[
            Embed(
                title="Mentoring",
                color=Color.orange(),
                description=info_mentee_description,
            ),
            Embed(description=info_mentor_description),
        ],
    )
    if info_message:
        messages_trash.remove(info_message)
        logger.info("Editing info message")
        discord_message = await discord_channel.fetch_message(info_message.id)
        with mutating_discord(discord_message) as proxy:
            await proxy.edit(**info_params)
    else:
        logger.info("Creating new info message")
        with mutating_discord(discord_channel) as proxy:
            await proxy.send(**info_params)

    logger.info("Deleting extraneous messages")
    for message in messages_trash:
        logger.debug(f"Deleting message #{message.id}: {message.content[:10]}…")
        try:
            discord_message = await discord_channel.fetch_message(message.id)
            with mutating_discord(discord_message) as proxy:
                await proxy.delete()
            message.delete_instance()
        except:
            logger.error(
                f"Could not delete message #{message.id}: {message.content[:10]}…"
            )
            raise


def get_mentor_params(mentor, thumbnail_url=None):
    content = f"{MENTOR_EMOJI} {mentor.user.mention}"
    if mentor.company:
        content += f" ({mentor.company})"

    description = ""
    if mentor.english_only:
        description += "🇬🇧 Pouze anglicky!\n"
    description += f"📖 {mentor.topics}\n"

    buttons = []
    if mentor.bio_url:
        buttons.append(
            ui.Button(
                emoji="👋",
                label="Představení",
                url=mentor.bio_url,
                style=ButtonStyle.secondary,
            )
        )
    if mentor.book_url:
        buttons.append(
            ui.Button(
                emoji="🗓",
                label="Rezervuj",
                url=mentor.book_url,
                style=ButtonStyle.secondary,
            )
        )
    else:
        buttons.append(
            ui.Button(
                emoji="<:discord:935790609023787018>",
                label="(Piš přímo přes Discord)",
                style=ButtonStyle.secondary,
                disabled=True,
            )
        )

    discord_embed = Embed(description=description)
    if thumbnail_url:
        discord_embed.set_thumbnail(url=thumbnail_url)

    return dict(content=content, embed=discord_embed, view=ui.View(*buttons))
