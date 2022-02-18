from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, is_discord_mutable
from juniorguru.models import ClubMessage, db


logger = loggers.get(__name__)


SYSTEM_MESSAGES_CHANNEL = 788823881024405544


@measure()
def main():
    run_discord_task('juniorguru.sync.returning_members.discord_task')


@db.connection_context()
async def discord_task(client):
    system_messages_channel = await client.fetch_channel(SYSTEM_MESSAGES_CHANNEL)
    for message in ClubMessage.channel_listing(SYSTEM_MESSAGES_CHANNEL):
        if message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
            logger.info(f'It looks like #{message.author.id} has returned')
            discord_message = await system_messages_channel.fetch_message(message.id)
            if is_discord_mutable():
                await discord_message.add_reaction('👋')
                await discord_message.add_reaction('🔄')


if __name__ == '__main__':
    main()
