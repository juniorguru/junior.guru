from datetime import datetime, timedelta

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import ClubMessage, with_db


logger = loggers.get('li_group')


LI_GROUP_CHANNEL = 839059491432431616
LI_GROUP_MESSAGE_PERIOD = timedelta(days=30)


@measure('li_group')
@with_db
@discord_task
async def main(client):
    ago_dt = datetime.utcnow() - LI_GROUP_MESSAGE_PERIOD
    logger.info(f'Message period is {repr(LI_GROUP_MESSAGE_PERIOD)}, calculated as {ago_dt.date()}')
    last_reminder_message = ClubMessage.last_bot_message(LI_GROUP_CHANNEL, '<:linkedin:915267970752712734>')
    if last_reminder_message:
        since_dt = last_reminder_message.created_at
        logger.info(f"Last reminder on {since_dt}")
        if since_dt.date() > ago_dt.date():
            logger.info(f"Stopping, {since_dt.date()} (last reminder) > {ago_dt.date()}")
            return  # stop
        else:
            logger.info(f"About to create reminder, {since_dt.date()} (last reminder) <= {ago_dt.date()}")
    else:
        logger.info('Last reminder not found')

    channel = await client.fetch_channel(LI_GROUP_CHANNEL)
    if DISCORD_MUTATIONS_ENABLED:
        await channel.send(content=(
            "<:linkedin:915267970752712734> Nezapomeň, že můžeš svou LinkedIn síť rozšířit o členy klubu. "
            "Přidej se do naší skupiny <https://www.linkedin.com/groups/13988090/>, "
            "díky které se pak můžeš snadno propojit s ostatními (a oni s tebou). "
            "Zároveň se ti bude logo junior.guru zobrazovat na profilu v sekci „zájmy”."
            "\n\n"
            "👀 Nevíme, jestli ti logo na profilu přidá nějaký kredit u recruiterů, ale vyloučeno to není! "
            "Minimálně jako poznávací znamení mezi námi by to zafungovat mohlo. "
            "Něco jako „Jé, koukám, že ty jsi taky chodila do skauta? Chodíš ještě? Jakou máš přezdívku?“"
        ), embed=None, embeds=[])
    else:
        logger.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


if __name__ == '__main__':
    main()
