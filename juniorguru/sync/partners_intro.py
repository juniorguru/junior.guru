from datetime import date, timedelta
from pathlib import Path
from textwrap import dedent

from discord import ButtonStyle, Color, Embed, File, ui
from jinja2 import Template

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (ClubChannelID, ClubClient, ClubEmoji,
                                         add_reactions, is_message_over_period_ago)
from juniorguru.lib.mutations import MutationsNotAllowedError, mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.partner import Partnership


BOT_REACTIONS = ['👋', '👍', '💕', '💰', '🎉']

IMAGES_DIR = Path('juniorguru/images')

DESCRIPTION_TEMPLATE = dedent('''
    {%- set partnership = partner.active_partnership() -%}
    **Tarif „{{ partnership.plan.name }}” {% for _ in range(partnership.plan.hierarchy_rank + 1) %}:star:{% endfor %}**

    {% for benefit in partnership.evaluate_benefits() -%}
    {{ benefit.text }}
    {% endfor %}
    {%- if partnership.student_role_id %}Posílají sem své studenty: <@&{{ partner.student_role_id }}>
    {% endif %}
    {%- if partnership.agreements_registry|length %}A ještě nějaká [další ujednání](https://junior.guru/open/{{ partner.slug }}#dalsi-ujednani)
    {% endif %}
    {% if partner.course_provider -%}
    ℹ️ Partnerství neznamená, že junior.guru doporučuje konkrétní kurzy, nebo že na ně nemáš psát recenze v klubu.
    {%- endif %}
''')


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content', 'partners', 'roles'])
def main():
    discord_sync.run(discord_task)


@db.connection_context()
async def discord_task(client: ClubClient):
    last_message = ClubMessage.last_bot_message(ClubChannelID.INTRO, ClubEmoji.PARTNER_INTRO)
    if is_message_over_period_ago(last_message, timedelta(weeks=1)):
        logger.info('Last partner intro message is more than one week old!')

        partners = list(get_partners_without_intro(Partnership.active_listing()))
        if partners:
            partners_names = ', '.join(partner.name for partner in partners)
            logger.info(f"Partners without intro: {partners_names}")
            partner = partners[0]
            logger.info(f"Introducing: {partner.name}")

            template = Template(DESCRIPTION_TEMPLATE)
            description = template.render(partner=partner)
            content = (
                f"{ClubEmoji.PARTNER_INTRO} Partnerství! "
                f"Firma {partner.name_markdown_bold} chce pomáhat juniorům. "
                f"Členové, které sem pošle, mají roli <@&{partner.role_id}> (aktuálně {len(partner.list_members)})."
            )
            embed = Embed(title=partner.name,
                          color=Color.dark_grey(),
                          description=description)
            embed.set_thumbnail(url=f"attachment://{Path(partner.poster_path).name}")
            file = File(IMAGES_DIR / partner.poster_path)
            buttons = [
                ui.Button(emoji='👉',
                          label=partner.name,
                          url=partner.url,
                          style=ButtonStyle.secondary),
                ui.Button(emoji='👀',
                          label='Detaily partnerství',
                          url=f'https://junior.guru/open/{partner.slug}',
                          style=ButtonStyle.secondary)
            ]
            channel = await client.fetch_channel(ClubChannelID.INTRO)
            try:
                with mutating_discord(channel, raises=True) as proxy:
                    message = await proxy.send(content=content, embed=embed, file=file, view=ui.View(*buttons))
            except MutationsNotAllowedError:
                pass
            else:
                await add_reactions(message, BOT_REACTIONS)
        else:
            logger.info('No partners to introduce')
    else:
        logger.info('Last partner intro message is less than one week old')


def get_partners_without_intro(active_partnerships, today=None):
    today = today or date.today()
    for partnership in active_partnerships:
        partner = partnership.partner
        if partner.intro:
            intro_created_on = partner.intro.created_at.date()
            is_intro_before_partnership = intro_created_on < partnership.starts_on
            is_barter = not partnership.expires_on
            is_intro_before_year_ago = today - intro_created_on > timedelta(days=365)
            if (is_intro_before_partnership or (is_barter and is_intro_before_year_ago)):
                yield partner
        else:
            yield partner
