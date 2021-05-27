import time
import random
import sys
from pathlib import Path

# The following is needed because /scripts/ is not a package (and I don't want it to be,
# I consider the directory to be just a drawer of random tools, related to the juniorguru
# app only very casually). Perhaps it's gonna change one day, but today is not that day.
sys.path.append(str(Path(__file__).parent.parent))
from juniorguru.lib.club import discord_task, emoji_name


@discord_task
async def main(client, message_url, winners_count):
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
    for i in range(5):
        print('The winners are…')
        time.sleep(1 * i)
    for user in random.sample(users, winners_count):
        print(f'🏆 {user.display_name} (id #{user.id})')


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
