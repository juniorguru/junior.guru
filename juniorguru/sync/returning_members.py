from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import ClubMessage


log = get_log('returning_members')


SYSTEM_MESSAGES_CHANNEL = 788823881024405544


@discord_task
async def main(client):
    system_messages_channel = await client.fetch_channel(SYSTEM_MESSAGES_CHANNEL)
    for message in ClubMessage.channel_listing(SYSTEM_MESSAGES_CHANNEL):
        if message.type == 'new_member' and message.author.first_seen_on() < message.created_at.date():
            log.info(f'It looks like {message.author.display_name} has returned')
            discord_message = await system_messages_channel.fetch_message(message.id)
            if DISCORD_MUTATIONS_ENABLED:
                await discord_message.add_reaction('👋')
                await discord_message.add_reaction('🔄')
            else:
                log.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


if __name__ == '__main__':
    main()
