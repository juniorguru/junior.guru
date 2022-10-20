from datetime import date
from operator import attrgetter
from textwrap import dedent

import feedparser
import requests
from discord import Color, Embed

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task
from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.models.club import (ClubDocumentedRole, ClubMessage,
                                    ClubSubscribedPeriod, ClubUser)
from juniorguru.models.company import Company
from juniorguru.models.event import Event


DASHBOARD_CHANNEL = 788822884948770846

TODAY = date.today()

BLOG_RSS_URL = 'https://honzajavorek.cz/feed.xml'

BLOG_WEEKNOTES_PREFIX = 'Týdenní poznámky'


logger = loggers.get(__name__)


@cli.sync_command(requires=['club-content',
                        'companies',
                        'events',
                        'subscriptions',
                        'roles'])
def main():
    run_discord_task('juniorguru.sync.dashboard.discord_task')


@db.connection_context()
async def discord_task(client):
    discord_channel = await client.fetch_channel(DASHBOARD_CHANNEL)

    sections = [
        render_basic_tips(),
        render_roles(),
        render_companies(),
        render_events(),
        render_open(),
    ]
    messages = sorted(ClubMessage.channel_listing_bot(DASHBOARD_CHANNEL),
                      key=attrgetter('created_at'))

    if len(messages) != len(sections):
        logger.warning('The scheme of sections seems to be different, purging the channel and creating new messages')
        if DISCORD_MUTATIONS_ENABLED:
            await discord_channel.purge()
            for section in sections:
                await discord_channel.send(embed=Embed(**section))
        else:
            logger.warning('Discord mutations not enabled')
    else:
        logger.info("Editing existing dashboard messages")
        if DISCORD_MUTATIONS_ENABLED:
            for i, message in enumerate(messages):
                discord_message = await discord_channel.fetch_message(message.id)
                await discord_message.edit(embed=Embed(**sections[i]))
        else:
            logger.warning('Discord mutations not enabled')


def render_basic_tips():
    return {
        'title': 'Základní tipy',
        'color': Color.yellow(),
        'description': dedent('''
            Klub je místo, kde můžeš spolu s ostatními posunout svůj rozvoj v oblasti programování, nebo s tím pomoci ostatním.

            👋 Tykáme si, ⚠️ [Pravidla chování](https://junior.guru/coc/), 💳 [Nastavení placení](https://juniorguru.memberful.com/account), 🤔 [Časté dotazy](https://junior.guru/faq/)
        ''').strip()
    }


def render_roles():
    return {
        'title': 'Role',
        'description': '\n'.join([
            f'{format_role(role)}\n' for role
            in ClubDocumentedRole.listing()
        ])
    }


def format_role(role):
    text = f'**{role.mention}**'
    if role.emoji:
        text += f' {role.emoji}'
    text += f'\n{role.description}'
    return text


def render_companies():
    return {
        'title': 'Spolupráce',
        'color': Color.dark_grey(),
        'description': 'Následující firmy se podílejí na financování provozu junior.guru. Někdy sem pošlou své lidi. Ti pak mají roli <@&837316268142493736> a k tomu ještě i roli vždy pro konkrétní firmu, například <@&938306918097747968>.\n\n' + ', '.join([
            f'✨ [{company.name}]({company.url})' for company
            in Company.listing(sort_by_name=True)
        ])
    }


def render_events():
    description = (
        'Všechno o akcích je [na webu](https://junior.guru/events/). '
        'Tady je akorát seznam odkazů na záznamy, ať je máš víc po ruce.\n\n'
    )
    description += '\n'.join([
        format_event(event)
        for event in Event.listing()
        if event.recording_url
    ])
    return {
        'title': 'Záznamy klubových akcí',
        'description': description,
    }


def format_event(event):
    return (
        f'📺 [{event.title}]({event.recording_url})\n'
        f'{event.start_at.date().day}.{event.start_at.date().month}.{event.start_at.date().year}, {event.bio_name}\n'
    )


def render_open():
    members_total_count = ClubUser.members_count()
    members_women_ptc = ClubSubscribedPeriod.women_ptc(TODAY)

    response = requests.get(BLOG_RSS_URL)
    response.raise_for_status()
    blog_entries = [entry for entry in feedparser.parse(response.content).entries
                    if entry.title.startswith(BLOG_WEEKNOTES_PREFIX)]
    blog_entries = sorted(blog_entries, key=attrgetter('published'), reverse=True)
    last_blog_entry = blog_entries[0]

    description = ', '.join([
        f'🙋 {members_total_count} členů v klubu, z toho asi {members_women_ptc} % žen',
        f'📝 [{last_blog_entry.title}]({last_blog_entry.link})',
        '📊 [Návštěvnost webu](https://simpleanalytics.com/junior.guru)',
        '<:github:842685206095724554> [Zdrojový kód](https://github.com/honzajavorek/junior.guru)',
        '📈 [Další čísla a grafy](https://junior.guru/open/)',
    ])
    description += '\n\n💡 Napadá tě vylepšení? Máš dotaz k fungování klubu? Šup s tím do <#806215364379148348>!'

    return {
        'title': 'Zákulisí junior.guru',
        'color': Color.greyple(),
        'description': description
    }
