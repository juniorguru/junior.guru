import random
import time

import click

from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, emoji_name


ROLE = 836959652100702248


logger = loggers.from_path(__file__)


@click.command()
@click.argument("message_url")
@click.argument("winners_count", type=int)
def main(message_url, winners_count):
    discord_task.run(draw_winners, message_url, winners_count)


async def draw_winners(client: ClubClient, message_url, winners_count):
    roles = await client.club_guild.fetch_roles()
    role = [role for role in roles if role.id == ROLE][0]
    logger.info(f"Limiting winners to only those with role '{role.name}'")

    message_url_parts = message_url.split("/")
    channel_id = int(message_url_parts[-2])
    channel = await client.fetch_channel(channel_id)
    logger.info(f"Message is in channel #{channel.name}")

    message_id = int(message_url_parts[-1])
    message = await channel.fetch_message(message_id)
    logger.info(
        f"Message has been posted by {message.author.display_name} at {message.created_at.isoformat()}+00:00"
    )

    reactions_count = sum([reaction.count for reaction in message.reactions])
    logger.info(f"Message has {reactions_count} reactions in total")
    users = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            logger.info(
                f"User {user.display_name} reacted with: {emoji_name(reaction.emoji)}"
            )
            if role in user.roles:
                users.add(user)
            else:
                logger.warning(
                    f"User {user.display_name} doesn't have role '{role.name}' and can't win!"
                )
    logger.info(f"{len(users)} users reacted")

    users_ids = sorted(user.id for user in users)
    winners_ids = random.sample(users_ids, winners_count)
    winners = [user for user in users if user.id in winners_ids]
    for i in range(1, 6):
        logger.info("The winners are…")
        time.sleep(1 * i)
    for user in winners:
        logger.info(f"🏆 {user.display_name} (id #{user.id})")
