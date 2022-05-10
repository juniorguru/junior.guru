from datetime import timedelta
from pathlib import Path
import asyncio

from discord import Embed, Colour
from strictyaml import CommaSeparated, Int, Map, Optional, Seq, Str, Url, Bool, load
from slugify import slugify

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, is_message_over_period_ago,
                                 run_discord_task)
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.sync.club_content import main as club_content_task


MENTORS_CHANNEL = 822415540843839488

DATA_PATH = Path(__file__).parent.parent / 'data' / 'mentors.yml'

SCHEMA = Seq(
    Map({
        'id': Int(),
        Optional('company'): Str(),
        'topics': CommaSeparated(Str()),
        Optional('english_only', default=False): Bool(),
        Optional('book_url'): Url(),
    })
)


logger = loggers.get(__name__)


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.mentors.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(MENTORS_CHANNEL, '💁')
    if is_message_over_period_ago(last_message, timedelta(days=30)):
        logger.info('Last message is more than one week old!')

        logger.info('Parsing YAML')
        yaml_records = [record.data for record in load(DATA_PATH.read_text(), SCHEMA)]
        logger.debug(f'Loaded {len(yaml_records)} mentors from YAML')

        logger.info('Downloading Discord member info')
        discord_members = await asyncio.gather(*[
            client.juniorguru_guild.fetch_member(yaml_record['id'])
            for yaml_record in yaml_records
        ])
        mentors = sorted(zip(discord_members, yaml_records), key=lambda mentor: slugify(mentor[0].display_name))

        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(MENTORS_CHANNEL)
            content = (
                '💁 Pomohlo by ti pravidelně si s někým na hodinku zavolat a probrat svůj postup? '
                'Následující členové se nabídli jako **mentoři**. Jak to funguje?\n'
                '\n'
                '1️⃣ 🧭 Stanov si dlouhodobější cíl, kterého chceš dosáhnout (např. porozumět API)\n'
                '2️⃣ 👋 Podle tématu si ze seznamu níže vyber mentorku/mentora. Rezervuj si čas na videohovor\n'
                '3️⃣ 🤝 Domluvte se, jak často si chcete volat (např. každé dva týdny) a jak dlouho (např. 5×)\n'
                '4️⃣ 📝 Aktivita je na tvé straně. Rezervuješ další schůzky a víš předem, co na nich chceš řešit\n'
                '5️⃣ 🚀 Mentorka/mentor radí, posouvá tě správným směrem, pomáhá ti dosáhnout cíle\n'
                '\n'
                '❤️ Mentoři jsou dobrovolníci, ne učitelé. Važ si jejich času a dopřej jim dobrý pocit, pokud pomohli\n'
                '<:discord:935790609023787018> Konkrétním lidem můžeš na Discordu psát přes `Ctrl+K` nebo `⌘+K`\n'
                '🙋 Není ti cokoliv jasné? Nefunguje něco? Piš <@!668226181769986078>\n'
            )
            embed_description_lines = [format_mentor(discord_member, yaml_record)
                                       for discord_member, yaml_record in mentors]
            embed_description_lines += [(
                '🦸 Chceš se taky nabídnout? Nejdřív si pusť [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski, ať víš jak na to. '
                'Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md). '
                'Potom napiš Honzovi, přidá tě do [seznamu](https://github.com/honzajavorek/junior.guru/blob/main/juniorguru/data/mentors.yml).'
            )]

            await channel.send(content=content, embed=Embed(colour=Colour.orange(),
                                                            description='\n'.join(embed_description_lines)))
        else:
            logger.warning('Discord mutations not enabled')


def format_mentor(discord_member, yaml_record):
    entry = f"**{discord_member.display_name}**"
    if yaml_record.get('company'):
        entry += f" – {yaml_record['company']}"
    entry += '\n'

    entry += f"💁 {', '.join(yaml_record['topics'])}\n"

    english = ' 🇬🇧 Pouze anglicky! ' if yaml_record['english_only'] else ''
    if yaml_record.get('book_url'):
        entry += f"🗓{english} [Rezervuj přes kalendář]({yaml_record['book_url']})"
    else:
        entry += f'<:discord:935790609023787018>{english} Soukromě napiš `{discord_member.name}#{discord_member.discriminator}`'
    entry += '\n'
    return entry
