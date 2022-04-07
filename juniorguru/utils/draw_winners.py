import time
import random

from invoke import task

from juniorguru.lib.club import run_discord_task, emoji_name


@task(name='draw_winners')
def main(context, message_url, winners_count):
    run_discord_task('juniorguru.utils.draw_winners.discord_task', message_url, winners_count)


async def discord_task(client, message_url, winners_count):
    message_url_parts = message_url.split('/')
    channel_id = int(message_url_parts[-2])
    channel = await client.fetch_channel(channel_id)
    print(f'Message is in channel #{channel.name}')

    message_id = int(message_url_parts[-1])
    message = await channel.fetch_message(message_id)
    print(f'Message has been posted by {message.author.display_name} at {message.created_at.isoformat()}+00:00')

    reactions_count = sum([reaction.count for reaction in message.reactions])
    print(f'Message has {reactions_count} reactions in total')
    users = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            print(f'User {user.display_name} reacted with: {emoji_name(reaction.emoji)}')
            users.add(user)
    print(f'{len(users)} users reacted')
    for i in range(1, 6):
        print('The winners are…')
        time.sleep(1 * i)
    for user in random.sample(users, winners_count):
        print(f'🏆 {user.display_name} (id #{user.id})')
