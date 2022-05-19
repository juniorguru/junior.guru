from datetime import timedelta

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, is_message_over_period_ago,
                                 run_discord_task)
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.sync.club_content import main as club_content_task


FORUM_CHANNEL = 878937534464417822

FORUM_EMOJI = '💡'


logger = loggers.get(__name__)


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.forum.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(FORUM_CHANNEL, FORUM_EMOJI)
    if is_message_over_period_ago(last_message, timedelta(days=7)):
        logger.info('Last message is more than one month old!')
        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(FORUM_CHANNEL)
            await channel.send(content=(
                f"{FORUM_EMOJI} Jak to tady funguje? Trochu jako <:stackoverflow:842465345670217778> **Stack Overflow**. "
                "Nevíš si s něčím rady? Pokusíme se ti pomoci. "
                "Nerozumíš něčemu? Pokusíme se ti to vysvětlit. "
                "\n\n"
                "🙋 Neboj se ptát! Zkus překonat strach, který jsme si všichni odnesli z českého nebo slovenského školství, "
                "popřípadě z Facebookových skupin. Tady se nikomu nevysmíváme. Nekoušeme. Neboj, nebudeš vypadat jako blbec. "
                "Nic jako hloupá otázka neexistuje. "
                "\n\n"
                "<:discordplus:976844345510617118> Jak se zeptat? Oprávnění v tomto kanálu vyžadují, aby se každá záležitost řešila "
                "v samostatném vlákně. Nové vlákno, anglicky _thread_, vytvoříš přes tlačítko „plus”."
            ))
            # TODO dobře položená otázka je skill, dobře položená otázka pomáhá ostatním ti dát užitečnou odpověď
            # https://stackoverflow.com/help/how-to-ask
            # https://jvns.ca/blog/good-questions/
        else:
            logger.warning('Discord mutations not enabled')
