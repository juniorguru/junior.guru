from juniorguru.sync import sync_task, club_content
from juniorguru.lib.club import run_discord_task, is_discord_mutable, is_message_over_month_ago
from juniorguru.models import ClubMessage, db


LI_GROUP_CHANNEL = 839059491432431616


@sync_task(club_content.main)
def main():
    run_discord_task('juniorguru.sync.li_group.discord_task')


@db.connection_context()
async def discord_task(client):
    message = ClubMessage.last_bot_message(LI_GROUP_CHANNEL, '<:linkedin:915267970752712734>')
    if is_message_over_month_ago(message) and is_discord_mutable():
        channel = await client.fetch_channel(LI_GROUP_CHANNEL)
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
