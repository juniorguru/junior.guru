from datetime import datetime, timedelta

from discord import Embed

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import ClubMessage, db


logger = loggers.get('mentoring')


MENTORING_CHANNEL = 878937534464417822


@measure('mentoring')
@discord_task
async def main(client):
    week_ago_dt = datetime.utcnow() - timedelta(weeks=1)
    with db:
        last_reminder_message = ClubMessage.last_bot_message(MENTORING_CHANNEL, ':teacher:')
    if last_reminder_message:
        since_dt = last_reminder_message.created_at
        logger.info(f"Last reminder on {since_dt}")
        if since_dt.date() > week_ago_dt.date():
            logger.info(f"Aborting, {since_dt.date()} (last reminder) > {week_ago_dt.date()} (week ago)")
            return  # abort
        else:
            logger.info(f"About to create reminder, {since_dt.date()} (last reminder) <= {week_ago_dt.date()} (week ago)")
    else:
        since_dt = week_ago_dt
        logger.info('Last reminder not found')

    channel = await client.fetch_channel(MENTORING_CHANNEL)
    if DISCORD_MUTATIONS_ENABLED:
        content = ":teacher: Nezapomeň, že kromě tohoto kanálu máš také možnost si rezervovat čas u mentorů z firem."
        embed_description = (
            'Kamarádi z **[Mews](https://www.mews.com/en/careers)** ti nabízí tyto konzultace: '
            '<@!289482229975875584> na frontend, '
            '<@!672433063690633216> na HR a komunity, '
            '<@!689498517995126847> na datovou analýzu, '
            '<@!854681167018459146> na cokoliv kolem IT, '
            '<@!868083628419199026> na backend, '
            '<@!869504117154934824> na QA a testování.\n'
            '➡️ [Rezervuj v kalendáři](https://outlook.office365.com/owa/calendar/Mewsprojuniorguru@mewssystems.com/bookings/)'
        )
        await channel.send(content=content, embed=Embed(description=embed_description))
    else:
        logger.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


if __name__ == '__main__':
    main()
