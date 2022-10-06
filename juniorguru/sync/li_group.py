from datetime import timedelta

from juniorguru.lib import loggers
from juniorguru.lib.club import (DISCORD_MUTATIONS_ENABLED, is_message_over_period_ago,
                                 run_discord_task)
from juniorguru.lib.tasks import sync_task
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage
from juniorguru.sync.club_content import main as club_content_task


LI_GROUP_CHANNEL = 839059491432431616


logger = loggers.get(__name__)


@sync_task(club_content_task)
def main():
    run_discord_task('juniorguru.sync.li_group.discord_task')


@db.connection_context()
async def discord_task(client):
    last_message = ClubMessage.last_bot_message(LI_GROUP_CHANNEL, '<:linkedin:915267970752712734>')
    if is_message_over_period_ago(last_message, timedelta(days=30)):
        logger.info('Last message is more than one month old!')
        if DISCORD_MUTATIONS_ENABLED:
            channel = await client.fetch_channel(LI_GROUP_CHANNEL)
            message = await channel.send(content=(
                "<:linkedin:915267970752712734> Nezapomeň, že můžeš svou LinkedIn síť rozšířit o členy klubu. "
                "Přidej se do naší skupiny <https://www.linkedin.com/groups/13988090/>, "
                "díky které se pak můžeš snadno propojit s ostatními (a oni s tebou). "
                "Zároveň se ti bude logo junior.guru zobrazovat na profilu v sekci „zájmy”."
                "\n\n"
                "👀 Nevíme, jestli ti logo na profilu přidá nějaký kredit u recruiterů, ale vyloučeno to není! "
                "Minimálně jako poznávací znamení mezi námi by to zafungovat mohlo. "
                "Něco jako „Jé, koukám, že ty jsi taky chodila do skauta? Chodíš ještě? Jakou máš přezdívku?“"
            ))
            await message.edit(suppress=True)
        else:
            logger.warning('Discord mutations not enabled')
