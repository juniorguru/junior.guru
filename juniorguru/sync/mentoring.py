from discord import Embed

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, is_discord_mutable, is_message_over_week_ago
from juniorguru.models import ClubMessage, db


MENTORING_CHANNEL = 878937534464417822


logger = loggers.get(__name__)


@measure()
def main():
    run_discord_task('juniorguru.sync.mentoring.discord_task')


@db.connection_context()
async def discord_task(client):
    message = ClubMessage.last_bot_message(MENTORING_CHANNEL, ':teacher:')
    if is_message_over_week_ago(message) and is_discord_mutable():
        channel = await client.fetch_channel(MENTORING_CHANNEL)
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
            'Kamarádi z **[Mews](https://www.mews.com/en/careers)** ti nabízí tyto konzultace: '
            '<@!289482229975875584> (Linh) na frontend, '
            '<@!672433063690633216> (Jan) na HR a komunity, '
            '<@!689498517995126847> (Markéta) na datovou analýzu, '
            '<@!854681167018459146> (Honza) na cokoliv kolem IT, '
            '<@!868083628419199026> (Radek) na backend, '
            '<@!869504117154934824> (Soňa) na QA a testování.\n'
            '➡️ [Rezervuj v kalendáři](https://outlook.office365.com/owa/calendar/Mewsprojuniorguru@mewssystems.com/bookings/)'
            '\n\n'
            'Kamarádi z **[Red Hatu](https://redhat.avature.net/juniorguru?jobId=20261&tags=dei+cz+-+juniorguru)** ti nabízí tyto konzultace: '
            '<@!380388619061559299> (Joža) na Python\n'
            '➡️ Rezervuj přes soukromou zprávu'
            '\n\n'
            '💡 **Tip:** Ať už jsi junior nebo mentor, pusť si parádní [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski. '
            'Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md).'
        )
        await channel.send(content=content, embed=Embed(description=embed_description))


if __name__ == '__main__':
    main()
