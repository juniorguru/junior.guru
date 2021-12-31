from datetime import datetime, timedelta

from discord import Embed

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import ClubMessage, with_db


logger = loggers.get('mentoring')


MENTORING_CHANNEL = 878937534464417822
MENTORING_MESSAGE_PERIOD = timedelta(weeks=1)


@measure('mentoring')
@with_db
@discord_task
async def main(client):
    ago_dt = datetime.utcnow() - MENTORING_MESSAGE_PERIOD
    logger.info(f'Message period is {repr(MENTORING_MESSAGE_PERIOD)}, calculated as {ago_dt.date()}')
    last_reminder_message = ClubMessage.last_bot_message(MENTORING_CHANNEL, ':teacher:')
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

    channel = await client.fetch_channel(MENTORING_CHANNEL)
    if DISCORD_MUTATIONS_ENABLED:
        content = (
            ":teacher: Nezapomeň, že si můžeš rezervovat čas u mentorů z firem. "
            "Jeden hovor může ušetřit tisíc písmenek na Discordu!"
            "\n\n"
            "💁 Chtějí pomáhat juniorům, tak se nabídli, že si s nimi může kdokoliv z klubu zavolat. "
            "Každý z nich rozumí jinému tématu, tak vybírej podle toho. "
            "Můžete si zavolat jednou, nebo si domluvit něco pravidelného. "
            "Neboj, je to neformální, přátelské, nezávazné, prostě pohodička. "
            "Kdo vyzkoušel, fakt si to pochvaluje!"
        )
        embed_description = (
            'Kamarádi z **[Mews](https://www.mews.com/en/careers?utm_source=juniorguru&utm_medium=club&utm_campaign=partnership)** ti nabízí tyto konzultace: '
            '<@!289482229975875584> (Linh) na frontend, '
            '<@!672433063690633216> (Jan) na HR a komunity, '
            '<@!689498517995126847> (Markéta) na datovou analýzu, '
            '<@!854681167018459146> (Honza) na cokoliv kolem IT, '
            '<@!868083628419199026> (Radek) na backend, '
            '<@!869504117154934824> (Soňa) na QA a testování.\n'
            '➡️ [Rezervuj v kalendáři](https://outlook.office365.com/owa/calendar/Mewsprojuniorguru@mewssystems.com/bookings/)'
            '\n\n'
            '💡 **Tip:** Ať už jsi junior nebo mentor, pusť si parádní [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski. '
            'Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md).'
        )
        await channel.send(content=content, embed=Embed(description=embed_description))
    else:
        logger.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


if __name__ == '__main__':
    main()
