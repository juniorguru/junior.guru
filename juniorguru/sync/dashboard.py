from operator import attrgetter
from textwrap import dedent
from datetime import date

from discord import Embed, Colour
import feedparser
import requests

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED, run_discord_task, JUNIORGURU_BOT
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubSubscribedPeriod, ClubUser
from juniorguru.models.company import Company
from juniorguru.models.event import Event
from juniorguru.sync.club_content import main as club_content_task
from juniorguru.sync.companies import main as companies_task
from juniorguru.sync.events import main as events_task
from juniorguru.sync.subscriptions import main as subscriptions_task


DASHBOARD_CHANNEL = 788822884948770846

TODAY = date.today()

BLOG_RSS_URL = 'https://honzajavorek.cz/feed.xml'

BLOG_WEEKNOTES_PREFIX = 'Týdenní poznámky'


logger = loggers.get(__name__)


@sync_task(club_content_task, companies_task, events_task, subscriptions_task)
def main():
    run_discord_task('juniorguru.sync.dashboard.discord_task')


@db.connection_context()
async def discord_task(client):
    logger.info("Preparing context for embeds")
    members_total_count = ClubUser.members_count()
    members_women_ptc = ClubSubscribedPeriod.women_ptc(TODAY)
    events = Event.listing()
    companies = Company.listing(sort_by_name=True)

    logger.info("Figuring out the last blog entry")
    response = requests.get(BLOG_RSS_URL)
    response.raise_for_status()
    blog_entries = [entry for entry in feedparser.parse(response.content).entries
                    if entry.title.startswith(BLOG_WEEKNOTES_PREFIX)]
    blog_entries = sorted(blog_entries, key=attrgetter('published'), reverse=True)
    last_blog_entry = blog_entries[0]

    logger.info("Preparing embeds")
    embeds = [
        {
            'title': 'Základní tipy',
            'colour': Colour.yellow(),
            'description': dedent(f'''
                Klub je místo, kde můžeš spolu s ostatními posunout svůj rozvoj v oblasti programování, nebo s tím pomoci ostatním. Místní bot <@{JUNIORGURU_BOT}> by tě měl postupně provést vším, co klub nabízí.

                👋 Tykáme si, ⚠️ [Pravidla chování](https://junior.guru/coc/), 💳 [Nastavení placení](https://juniorguru.memberful.com/account), 🤔 [Časté dotazy](https://junior.guru/faq/)
            ''').strip()
        },
        # {  TODO
        #     'title': 'Role',
        #     'colour': Colour.blurple(),
        #     'description': description('''
        #         Tralalala
        #     ''')
        # },
        {
            'title': 'Spolupráce',
            'colour': Colour.dark_grey(),
            'description': 'Následující firmy se podílejí na financování provozu junior.guru. Někdy sem pošlou své lidi. Ti pak mají roli <@&837316268142493736> a k tomu ještě i roli vždy pro konkrétní firmu, například <@&938306918097747968>.\n\n' + ', '.join([
                f'✨ [{company.name}]({company.url})' for company in companies
            ])
        },
        {
            'title': 'Záznamy klubových akcí',
            'description': 'Všechno o akcích je [na webu](https://junior.guru/events/). Tady je akorát seznam odkazů na záznamy, ať je máš víc po ruce.\n\n' + '\n'.join([
                (f'📺 [{event.title}]({event.recording_url})\n'
                 f'{event.start_at.date().day}.{event.start_at.date().month}.{event.start_at.date().year}, {event.bio_name}\n')
                for event in events
                if event.recording_url
            ])
        },
        {
            'title': 'Zákulisí junior.guru',
            'colour': Colour.greyple(),
            'description': ', '.join([
                f'🙋 {members_total_count} členů, z toho asi {members_women_ptc} % žen',
                f'📝 [{last_blog_entry.title}]({last_blog_entry.link})',
                '📊 [Návštěvnost webu](https://simpleanalytics.com/junior.guru)',
                '<:github:842685206095724554> [Zdrojový kód](https://github.com/honzajavorek/junior.guru)',
                '📈 [Další čísla a grafy](https://junior.guru/open/)',
            ]) + '\n\n💡 Napadá tě vylepšení? Máš dotaz k fungování klubu? Šup s tím do <#806215364379148348>!'
        },
    ]

    message = ClubMessage.last_bot_message(DASHBOARD_CHANNEL)
    if message:
        logger.info("Editing dashboard message")
        if DISCORD_MUTATIONS_ENABLED:
            discord_channel = await client.fetch_channel(DASHBOARD_CHANNEL)
            discord_message = await discord_channel.fetch_message(message.id)
            await discord_message.edit(embeds=[Embed(**params) for params in embeds])
        else:
            logger.warning('Discord mutations not enabled')
    else:
        logger.info("Creating new dashboard message")
        if DISCORD_MUTATIONS_ENABLED:
            discord_channel = await client.fetch_channel(DASHBOARD_CHANNEL)
            await discord_channel.send(embeds=[Embed(**params) for params in embeds])
        else:
            logger.warning('Discord mutations not enabled')
