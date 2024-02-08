from datetime import date

import click
from discord import ScheduledEvent
from juniorguru.lib import discord_task, loggers
from juniorguru.cli.sync import main as cli
from juniorguru.lib.discord_club import ClubChannelID, ClubClient, parse_channel
from juniorguru.models.club import ClubMessage
from juniorguru.lib.mutations import mutating_discord


logger = loggers.from_path(__file__)


TALK_EMOJI = "💬"


@cli.sync_command(dependencies=["club-content"])
@click.option("--channel", "channel_id", default="announcements", type=parse_channel)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
def main(channel_id: int, today: date):
    message = ClubMessage.last_bot_message(channel_id, starting_emoji=TALK_EMOJI)
    if message and message.created_at.date() == today:
        logger.info("Talk announcement already exists")
        return
    discord_task.run(announce_talk, channel_id, today)


async def announce_talk(client: ClubClient, channel_id: int, today: date):
    talks = filter(is_talk, client.club_guild.scheduled_events)
    talks = filter(lambda talk: talk.start_time.date() == today, talks)
    try:
        talk = next(talks)
    except StopIteration:
        logger.info("No talk today")
        return

    logger.info(f"Announcing talk {talk.url}")
    text = f"{TALK_EMOJI} **Today's talk**: {talk.url}"
    # TODO udělat tip do klub tipy, kam dám většinu toho textu
    # znamená to mít aktuální link na tip
    # znamená to uložit si někam link tip, když ho vytvářím, do db, a dát tipy do závislostí tohoto skriptu
    #
    #
    # Ahojte, dneska večer bude opět pondělní povídání bla bla bla. Na viděnou minimámálně s {interested-users}
    #
    #
    # Jako každé pondělí se i dnes setkáme v online klubovně v rámci eventu Pondělní povídání, viz events (události). Až na pár výjimek není striktně daný program.
    #
    # Po sedmé zpravidla začínáme s úvodním "kolečkem", kdy každý účastník má kolem 1:30 min, aby ostatním řekl, čemu se zrovna věnuje, s čím bojuje atd. Když je někdo na Pondělním povídání poprvé, tak se v rámci této aktivity také představí.
    #
    # Po úvodním kolečku volně pokračujeme na jakékoliv téma. Jestli už teď víš, co bys chtěl/a dnes večer probrat, tak klidně napiš tady do vlákna 😉 Můžeme se tomu pověnovat přednostně. V případě většího počtu účastníků a/nebo témat se rozdělíme do více voice chatů.
    #
    # Většinou má alespoň tak půlka lidí zapnutou kameru, ale není to pravidlem. Jestli se chceš připojit a jen poslouchat, tak to napiš do chatu, nebo mě do soukromé zprávy. Jinak se často s nově příchozí/m pokusím interagovat, když je prostor.
    #
    # @ყυɾαყƙσ, @YpsiX 🧅, @David Knotek, @Kuba, @Dan Srb, @Dale, @Petr Kašička, @nathalie6811, @Petr Kopecký, @Wewa na viděnou, slyšenou večer 👋
    #
    #
    # Zakládám skupinku pro odkládání témat a jakoukoliv konverzaci ohledně pondělního povídání, když zrovna nejsme v klubovně, nebo jiné z roomek.
    # https://discord.com/channels/769966886598737931/1198999483309117582/1198999483309117582

    mentions = sorted([user.mention async for user in talk.subscribers()])
    if mentions:
        text += f"\n\nUž teď to vypadá, že na akci potkáš {' '.join(mentions)}"

    channel = await client.fetch_channel(channel_id)
    with mutating_discord(channel) as proxy:
        await proxy.send(text)


def is_talk(scheduled_event: ScheduledEvent) -> bool:
    location_id = getattr(scheduled_event.location.value, "id", None)
    return location_id == ClubChannelID.CLUBHOUSE
