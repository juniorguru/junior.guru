import re
from pathlib import Path
from datetime import timedelta, date

from discord import Embed, File, Colour

from juniorguru.lib.tasks import sync_task
from juniorguru.sync.club_content import main as club_content_task
from juniorguru.sync.companies import main as companies_task
from juniorguru.sync.roles import main as roles_task
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, DISCORD_MUTATIONS_ENABLED, is_message_over_period_ago, BOT_CHANNEL, JOBS_CHANNEL
from juniorguru.models import ClubMessage, Company, db


MESSAGE_EMOJI = '👋'

COMPANIES_INTRO_LAUNCH_ON = date(2022, 4, 1)

POSTERS_DIR = Path(__file__).parent.parent / 'images' / 'posters-companies'


logger = loggers.get(__name__)


@sync_task(
    # club_content_task,
    # companies_task,
    # roles_task,
)
def main():
    run_discord_task('juniorguru.sync.companies_intro.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(BOT_CHANNEL, '🤝')
    if is_message_over_period_ago(last_message, timedelta(weeks=1)):
        logger.info('Last company intro message is more than one week old!')

        companies = [company for company in Company.listing()
                     if doesnt_have_intro(company)]
        if companies:
            logger.debug(f'Choosing from {len(companies)} companies to announce')
            company = sorted(companies, key=sort_key)[0]

            logger.debug(f'Decided to announce {company!r}')
            if DISCORD_MUTATIONS_ENABLED:
                channel = await client.fetch_channel(BOT_CHANNEL)
                content = (
                    f"{MESSAGE_EMOJI} Kamarádi z firmy {company_name_formatted(company.name)} "
                    f"se rozhodli podpořit klub a jsou tady s námi!"
                )
                if company.starts_on < COMPANIES_INTRO_LAUNCH_ON and (date.today() - company.starts_on).days > 30:
                    content += (
                        ' 🐣 Sice to píšu jako novinku, ale ve skutečnosti klub podporují už od '
                        f'{company.starts_on.day}.{company.starts_on.month}.{company.starts_on.year}. '
                        'Jenže tehdy jsem bylo malé kuřátko, které ještě neumělo vítat firmy.'
                    )

                embed_description_lines = [
                    f"ℹ️ Víc **o firmě** najdeš na [{clean_url(company.url)}]({company.url})",
                    f"💕 Chtějí **pomáhat** juniorům! Mají roli <@&{company.role_id}>",
                    "🛡 Mají **logo** na [stránce klubu](https://junior.guru/club/)",
                ]
                if company.is_sponsoring_handbook:
                    embed_description_lines.append('📖 Mají **logo** na [příručce pro juniory](https://junior.guru/handbook/)')
                if company.job_slots_count:
                    embed_description_lines.append(f'🧑‍💻 Mají **inzeráty** v <#{JOBS_CHANNEL}> a [na webu](https://junior.guru/jobs/)')
                if company.student_role_id:
                    embed_description_lines.append(f'🧑‍🎓 Posílají sem své **studenty**: <@&{company.student_role_id}>')
                embed_description_lines += [
                    '💰 **Financují** práci na [příručce pro juniory](https://junior.guru/handbook/)',
                    '\n💡 Jak přesně funguje firemní členství? Mrkni do [FAQ](https://junior.guru/faq/#spoluprace-s-firmami-a-komunitami)',
                ]

                image_filename = 'c29bd3bd01915ab3289c293ef8cf05758669acbdb9070ac0bdacf23fe904e039.png'
                embed = Embed(colour=Colour.dark_grey(),
                              description='\n'.join(embed_description_lines))
                embed.set_thumbnail(url=f"attachment://{image_filename}")
                file = File(POSTERS_DIR / image_filename)

                await channel.send(content=content, embed=embed, file=file)
            else:
                logger.warning('Discord mutations not enabled')
        else:
            logger.info('No companies to announce')
    else:
        logger.info('Last company intro message is less than one week old')


def company_name_formatted(company_name):
    return f'**{company_name}**'


def doesnt_have_intro(company):
    message = ClubMessage.last_bot_message(BOT_CHANNEL, MESSAGE_EMOJI,
                                           company_name_formatted(company.name))
    return is_message_over_period_ago(message, timedelta(days=365))


def sort_key(company, today=None):
    today = today or date.today()
    expires_on = (company.expires_on or date(3000, 1, 1))
    expires_in_days = (expires_on - today).days
    started_days_ago = (today - company.starts_on).days
    return (expires_in_days if expires_in_days <= 30 else 1000,
            started_days_ago,
            company.name)


def clean_url(url):
    return re.sub(r'/$', '', re.sub(r'^https?://(www\.)?', '', url))
