import asyncio
from datetime import date, timedelta
from pathlib import Path

import click
from discord import Color, Embed, File

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, INTRO_CHANNEL, JOBS_CHANNEL,
                                 is_message_over_period_ago, run_discord_task)
from juniorguru.cli.sync import Command
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.company import Company


MESSAGE_EMOJI = '👋'

BOT_REACTIONS = ['👋', '👍', '💕', '💰']

COMPANIES_INTRO_LAUNCH_ON = date(2022, 4, 1)

IMAGES_DIR = Path(__file__).parent.parent / 'images'


logger = loggers.get(__name__)


@click.command(cls=Command, requires=['club-content',
                        'companies',
                        'roles'])
def main():
    run_discord_task('juniorguru.sync.companies_intro.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(INTRO_CHANNEL, MESSAGE_EMOJI)
    if is_message_over_period_ago(last_message, timedelta(weeks=1)):
        logger.info('Last company intro message is more than one week old!')

        companies = [company for company in Company.listing()
                     if doesnt_have_intro(company)]
        if companies:
            logger.debug(f'Choosing from {len(companies)} companies to announce')
            company = sorted(companies, key=sort_key)[0]

            logger.debug(f'Decided to announce {company!r}')
            if DISCORD_MUTATIONS_ENABLED:
                channel = await client.fetch_channel(INTRO_CHANNEL)
                content = (
                    f"{MESSAGE_EMOJI} "
                    f"Kamarádi z {company_name_formatted(company.name)} se rozhodli podpořit klub a jsou tady s námi! "
                    f"Mají roli <@&{company.role_id}>."
                )
                if company.starts_on < COMPANIES_INTRO_LAUNCH_ON and (date.today() - company.starts_on).days > 30:
                    content += (
                        ' 🐣 Sice to píšu jako novinku, ale ve skutečnosti klub podporují už od '
                        f'{company.starts_on.day}.{company.starts_on.month}.{company.starts_on.year}. '
                        'Jenže tehdy jsem bylo malé kuřátko, které ještě neumělo vítat firmy.'
                    )

                embed_description_lines = [
                    f"ℹ️ Víc o firmě najdeš na [jejich webu]({company.url})",
                    "🛡 Mají logo na [stránce klubu](https://junior.guru/club/)",
                ]
                if company.is_sponsoring_handbook:
                    embed_description_lines.append('📖 Mají logo na [příručce pro juniory](https://junior.guru/handbook/)')
                if company.job_slots_count:
                    embed_description_lines.append(f'🧑‍💻 Mají inzeráty v <#{JOBS_CHANNEL}> a [na webu](https://junior.guru/jobs/)')
                if company.student_role_id:
                    embed_description_lines.append(f'🧑‍🎓 Posílají sem své studenty: <@&{company.student_role_id}>')
                embed_description_lines += [
                    "💕 Chtějí pomáhat juniorům!",
                    '💰 Financují práci na [příručce pro juniory](https://junior.guru/handbook/)',
                    '\nJak přesně funguje spolupráce s firmami? Mrkni do [FAQ](https://junior.guru/faq/#firmy)',
                ]

                embed = Embed(title=company.name, color=Color.dark_grey(),
                              description='\n'.join(embed_description_lines))
                embed.set_thumbnail(url=f"attachment://{Path(company.poster_path).name}")
                file = File(IMAGES_DIR / company.poster_path)

                message = await channel.send(content=content, embed=embed, file=file)
                await asyncio.gather(*[message.add_reaction(emoji) for emoji in BOT_REACTIONS])
            else:
                logger.warning('Discord mutations not enabled')
        else:
            logger.info('No companies to announce')
    else:
        logger.info('Last company intro message is less than one week old')


def company_name_formatted(company_name):
    return f'**{company_name}**'


def doesnt_have_intro(company):
    message = ClubMessage.last_bot_message(INTRO_CHANNEL, MESSAGE_EMOJI,
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
