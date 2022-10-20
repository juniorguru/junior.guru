from pathlib import Path

from discord import ButtonStyle, Color, Embed, ui
from strictyaml import Bool, Int, Map, Optional, Seq, Str, Url, load

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, MENTORING_CHANNEL,
                                 run_discord_task)
from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.models.mentor import Mentor


MENTOR_EMOJI = '💁'

INFO_EMOJI = '💡'

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


@cli.sync_command(requires=['club-content'])
def main():
    run_discord_task('juniorguru.sync.mentoring.discord_task')


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

    messages_trash = set(ClubMessage.channel_listing(MENTORING_CHANNEL))
    info_message = ClubMessage.last_bot_message(MENTORING_CHANNEL, INFO_EMOJI)
    discord_channel = await client.fetch_channel(MENTORING_CHANNEL)

    logger.info('Syncing mentors')
    for mentor in mentors:
        discord_member = await client.juniorguru_guild.fetch_member(mentor.user.id)
        mentor_params = get_mentor_params(mentor, thumbnail_url=discord_member.display_avatar.url)

        message = ClubMessage.last_bot_message(MENTORING_CHANNEL, MENTOR_EMOJI, mentor.user.mention)
        if message:
            messages_trash.remove(message)
            logger.info(f"Editing existing message for mentor {mentor.name}")
            if DISCORD_MUTATIONS_ENABLED:
                discord_message = await discord_channel.fetch_message(message.id)
                await discord_message.edit(**mentor_params)
            else:
                logger.warning('Discord mutations not enabled')
            mentor.message_url = message.url
            mentor.save()
        else:
            logger.info(f"Creating a new message for mentor {mentor.name}")
            if DISCORD_MUTATIONS_ENABLED:
                if info_message:
                    logger.info("Deleting info message")
                    info_discord_message = await discord_channel.fetch_message(info_message.id)
                    await info_discord_message.delete()
                    info_message.delete_instance()
                    info_message = None
                discord_message = await discord_channel.send(**mentor_params)
                mentor.message_url = discord_message.jump_url
                mentor.save()
            else:
                logger.warning('Discord mutations not enabled')

    logger.info('Syncing info')
    info_content = f'{INFO_EMOJI} Co to tady je? Jak to funguje?'
    info_mentee_description = ('Pomohlo by ti pravidelně si s někým na hodinku zavolat a probrat svůj postup? '
                               'Předchozí zprávy v tomto kanálu představují seznam **mentorů**, kteří se k takové pomoci nabídli. '
                               'Postupuj následovně:\n'
                               '\n'
                               '1️⃣ 🧭 Stanov si dlouhodobější cíl (např. porozumět API)\n'
                               '2️⃣ 👋 Podle tématu si vyber mentorku/mentora a rezervuj si čas na videohovor\n'
                               '3️⃣ 🤝 Domluvte se, jak často si budete volat (např. každé dva týdny, půl roku)\n'
                               '4️⃣ 📝 Rezervuj jednotlivé schůzky a předem měj jasno, co na nich chceš řešit\n'
                               '5️⃣ 🚀 Mentor ti pomáhá dosáhnout cíle. Radí a posouvá tě správným směrem\n'
                               '\n'
                               '❤️ Mentoři jsou dobrovolníci, ne placení učitelé. Aktivita je na tvé straně. Važ si jejich času a dopřej jim dobrý pocit, pokud pomohli.\n')
    info_mentor_description = ('🦸 I ty můžeš mentorovat! '
                               'Nemusíš mít 10 let zkušeností v oboru. '
                               'Pusť si [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski, ať víš, co od toho čekat. '
                               'Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md). '
                               'Potom napiš Honzovi, přidá tě do [seznamu](https://github.com/honzajavorek/junior.guru/blob/main/juniorguru/data/mentors.yml).')
    info_params = dict(content=info_content,
                       embeds=[Embed(title='Mentoring', color=Color.orange(),
                                     description=info_mentee_description),
                               Embed(description=info_mentor_description)])
    if info_message:
        messages_trash.remove(info_message)
        logger.info("Editing info message")
        discord_message = await discord_channel.fetch_message(info_message.id)
        if DISCORD_MUTATIONS_ENABLED:
            await discord_message.edit(**info_params)
        else:
            logger.warning('Discord mutations not enabled')
    else:
        logger.info("Creating new info message")
        if DISCORD_MUTATIONS_ENABLED:
            await discord_channel.send(**info_params)
        else:
            logger.warning('Discord mutations not enabled')

    logger.info('Deleting extraneous messages')
    for message in messages_trash:
        logger.debug(f'Deleting message #{message.id}: {message.content[:10]}…')
        if DISCORD_MUTATIONS_ENABLED:
            discord_message = await discord_channel.fetch_message(message.id)
            await discord_message.delete()
            message.delete_instance()
        else:
            logger.warning('Discord mutations not enabled')


def get_mentor_params(mentor, thumbnail_url=None):
    content = f'{MENTOR_EMOJI} {mentor.user.mention}'
    if mentor.company:
        content += f' ({mentor.company})'

    description = ''
    if mentor.english_only:
        description += "🇬🇧 Pouze anglicky!\n"
    description += f"📖 {mentor.topics}\n"

    if mentor.book_url:
        view = ui.View(ui.Button(emoji='🗓',
                                 label='Rezervuj přes kalendář',
                                 url=mentor.book_url,
                                 style=ButtonStyle.secondary))
    else:
        view = ui.View(ui.Button(emoji='<:discord:935790609023787018>',
                                 label='(Piš přímo přes Discord)',
                                 style=ButtonStyle.secondary,
                                 disabled=True))

    discord_embed = Embed(description=description)
    if thumbnail_url:
        discord_embed.set_thumbnail(url=thumbnail_url)

    return dict(content=content, embed=discord_embed, view=view)
