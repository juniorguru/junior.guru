from datetime import timedelta
from pathlib import Path

from discord import Embed, Colour
from strictyaml import Int, Map, Optional, Seq, Str, Url, Bool, load

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, is_message_over_period_ago,
                                 run_discord_task)
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.mentor import Mentor
from juniorguru.sync.club_content import main as club_content_task


MENTORS_CHANNEL = 822415540843839488

MESSAGE_EMOJI = '💁'

DATA_PATH = Path(__file__).parent.parent / 'data' / 'mentors.yml'

SCHEMA = Seq(
    Map({
        'id': Int(),
        'name': Str(),
        Optional('company'): Str(),
        'topics': Str(),
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
    logger.info('Setting up db table')
    Mentor.drop_table()
    Mentor.create_table()

    logger.info('Parsing YAML')
    for yaml_record in load(DATA_PATH.read_text(), SCHEMA):
        Mentor.create(user=yaml_record.data['id'], **yaml_record.data)
    mentors = Mentor.listing()
    logger.debug(f'Loaded {len(mentors)} mentors from YAML')

    last_message = ClubMessage.last_bot_message(MENTORS_CHANNEL, MESSAGE_EMOJI)
    if is_message_over_period_ago(last_message, timedelta(days=30)):
        logger.info('Last message in the mentors channel is more than one month old!')

        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(MENTORS_CHANNEL)
            content = (
                f'{MESSAGE_EMOJI} Pomohlo by ti pravidelně si s někým na hodinku zavolat a probrat svůj postup? '
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
            embed_description_lines = list(map(format_mentor, mentors))
            embed_description_lines.append(
                '🦸 Chceš se taky nabídnout? Nejdřív si pusť [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski, ať víš jak na to. '
                'Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md). '
                'Potom napiš Honzovi, přidá tě do [seznamu](https://github.com/honzajavorek/junior.guru/blob/main/juniorguru/data/mentors.yml).'
            )

            await channel.send(content=content, embed=Embed(colour=Colour.orange(),
                                                            description='\n'.join(embed_description_lines)))
        else:
            logger.warning('Discord mutations not enabled')


def format_mentor(mentor):
    entry = f"**{mentor.user.display_name}**"
    if mentor.company:
        entry += f" – {mentor.company}"
    entry += '\n'

    entry += f"💁 {mentor.topics}\n"

    english = ' 🇬🇧 Pouze anglicky! ' if mentor.english_only else ''
    if mentor.book_url:
        entry += f"🗓{english} [Rezervuj přes kalendář]({mentor.book_url})"
    else:
        entry += f'<:discord:935790609023787018>{english} Soukromě napiš `{mentor.tag}`'
    entry += '\n'
    return entry
