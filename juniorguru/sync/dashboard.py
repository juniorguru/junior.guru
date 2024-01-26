from datetime import date
from operator import attrgetter
from textwrap import dedent

from discord import Color, Embed

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_task, loggers
from juniorguru.lib.discord_club import ClubChannelID, ClubClient
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.blog import BlogArticle
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.models.subscription import SubscriptionActivity


TODAY = date.today()

EVENTS_LIMIT = 10


logger = loggers.from_path(__file__)


@cli.sync_command(
    dependencies=[
        "club-content",
        "subscriptions",
        "blog",
    ]
)
def main():
    discord_task.run(sync_dashboard)


@db.connection_context()
async def sync_dashboard(client: ClubClient):
    discord_channel = await client.fetch_channel(ClubChannelID.DASHBOARD)

    sections = [
        render_basic_tips(),
        render_roles(),
        render_partners(),
        render_events(),
        render_open(),
    ]
    messages = sorted(
        ClubMessage.channel_listing(ClubChannelID.DASHBOARD, by_bot=True),
        key=attrgetter("created_at"),
    )

    if len(messages) != len(sections):
        logger.warning(
            "The scheme of sections seems to be different, purging the channel and creating new messages"
        )
        with mutating_discord(discord_channel) as proxy:
            await proxy.purge()
            for section in sections:
                await proxy.send(embed=Embed(**section))
    else:
        logger.info("Editing existing dashboard messages")
        for i, message in enumerate(messages):
            discord_message = await discord_channel.fetch_message(message.id)
            with mutating_discord(discord_message) as proxy:
                await proxy.edit(embed=Embed(**sections[i]))


def render_basic_tips():
    return {
        "title": "Základní tipy",
        "color": Color.yellow(),
        "description": dedent(
            """
            Klub je místo, kde můžeš spolu s ostatními posunout svůj rozvoj v oblasti programování, nebo s tím pomoci ostatním.

            👋 Tykáme si, ⚠️ [Pravidla chování](https://junior.guru/coc/), 💳 [Nastavení placení](https://juniorguru.memberful.com/account), 🤔 [Časté dotazy](https://junior.guru/faq/)
        """
        ).strip(),
    }


def render_roles():
    return {
        "title": "Role",
        "description": "Přesunuto do <#1174338887406075954>.",
    }


def render_partners():
    return {
        "title": "Partneři",
        "color": Color.dark_grey(),
        "description": "Přesunuto do <#1177200287107264554>.",
    }


def render_events():
    return {
        "title": "Záznamy klubových akcí",
        "description": "Přesunuto do <#1169636415387205632>.",
    }


def render_open():
    members_total_count = ClubUser.members_count()
    members_women_ptc = SubscriptionActivity.active_women_ptc(TODAY)
    blog_article = BlogArticle.latest()

    description = ", ".join(
        [
            f"🙋 {members_total_count} členů v klubu, z toho asi {members_women_ptc} % žen",
            f"📝 [{blog_article.title}]({blog_article.url})",
            "📊 [Návštěvnost webu](https://simpleanalytics.com/junior.guru)",
            "<:github:842685206095724554> [Zdrojový kód](https://github.com/juniorguru/junior.guru)",
            "📈 [Další čísla a grafy](https://junior.guru/open/)",
        ]
    )
    description += "\n\n💡 Napadá tě vylepšení? Máš dotaz k fungování klubu? Šup s tím do <#806215364379148348>!"

    return {
        "title": "Zákulisí junior.guru",
        "color": Color.greyple(),
        "description": description,
    }
