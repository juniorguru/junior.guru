import asyncio
from datetime import date, timedelta
from pathlib import Path
from textwrap import dedent

from discord import Color, Embed, File, ui, ButtonStyle
from jinja2 import Template

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED
from juniorguru.lib.club import EMOJI_PARTNER_INTRO, INTRO_CHANNEL, is_message_over_period_ago, run_discord_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.partner import Partner


BOT_REACTIONS = ['👋', '👍', '💕', '💰']

IMAGES_DIR = Path(__file__).parent.parent / 'images'

DESCRIPTION_TEMPLATE = dedent('''
    {%- set partnership = partner.active_partnership() -%}
    Tarif **{{ partnership.plan.name }}** {% for _ in range(partnership.plan.hierarchy_rank + 1) %}:star:{% endfor %}

    ℹ️ Mrkni na [jejich web]({{ partner.url }})
    🙂 Aktuálně členů v klubu: {{ partner.list_members|length }}
    🗓️ Od {{ '{:%-d.%-m.%Y}'.format(partnership.starts_on) }} do
    {%- if partnership.expires_on %} {{ '{:%-d.%-m.%Y}'.format(partnership.expires_on) }}{% else %} odvolání{% endif %}
''')


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content', 'partners', 'roles'])
def main():
    run_discord_task('juniorguru.sync.partners_intro.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(INTRO_CHANNEL, EMOJI_PARTNER_INTRO)
    if is_message_over_period_ago(last_message, timedelta(weeks=1)):
        logger.info('Last partner intro message is more than one week old!')

        partners = [partner for partner in Partner.active_listing()
                    if is_message_over_period_ago(partner.intro, timedelta(days=365))]
        if partners:
            logger.debug(f'Choosing from {len(partners)} partners to announce')
            partner = sorted(partners, key=sort_key)[0]
            logger.debug(f'Decided to announce {partner!r}')

            template = Template(DESCRIPTION_TEMPLATE)
            description = template.render(partner=partner)
            channel = await client.fetch_channel(INTRO_CHANNEL)
            content = (
                f"{EMOJI_PARTNER_INTRO} "
                f"Kamarádi z {partner.name_markdown_bold} podporují klub! "
                f"Mají roli <@&{partner.role_id}>."
            )
            embed = Embed(title=partner.name, color=Color.dark_grey(),
                            description=description)
            embed.set_thumbnail(url=f"attachment://{Path(partner.poster_path).name}")
            file = File(IMAGES_DIR / partner.poster_path)
            button = ui.Button(label='Detaily partnerství',
                                url=f'https://junior.guru/open/{partner.slug}',
                                style=ButtonStyle.secondary)
            if DISCORD_MUTATIONS_ENABLED:
                message = await channel.send(content=content, embed=embed, file=file, view=ui.View(button))
                await asyncio.gather(*[message.add_reaction(emoji) for emoji in BOT_REACTIONS])
            else:
                logger.warning('Discord mutations not enabled')
        else:
            logger.info('No partners to announce')
    else:
        logger.info('Last partner intro message is less than one week old')


def sort_key(partner, today=None):
    today = today or date.today()
    partnership = partner.active_partnership()
    expires_on = (partnership.expires_on or date(3000, 1, 1))
    expires_in_days = (expires_on - today).days
    started_days_ago = (today - partnership.starts_on).days
    return (expires_in_days if expires_in_days <= 30 else 1000,
            started_days_ago,
            partner.name)
