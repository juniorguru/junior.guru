import re
from urllib.parse import urlparse
from pathlib import Path
from io import BytesIO
from collections import Counter

import arrow
from PIL import Image

from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, exclude_categories, exclude_bots, DEFAULT_EXCLUDED_MEMBERS
from juniorguru.models import Member, db


log = get_log('members')


IMAGES_PATH = Path(__file__).parent.parent / 'data' / 'images'
AVATARS_PATH = IMAGES_PATH / 'avatars'
SIZE_PX = 60
STATS_PERIOD_DAYS = 30


@discord_task
async def main(client):
    AVATARS_PATH.mkdir(exist_ok=True, parents=True)
    for path in AVATARS_PATH.glob('*'):
        path.unlink()

    with db:
        Member.drop_table()
        Member.create_table()

    for member in exclude_bots([member async for member in client.juniorguru_guild.fetch_members(limit=None)]):
        log.info(f'Member {member.display_name} {member.id}')
        avatar_url = str(member.avatar_url)
        if is_default_avatar(avatar_url):
            avatar_path = None
        else:
            buffer = BytesIO()
            await member.avatar_url.save(buffer)
            image = Image.open(buffer)
            image = image.resize((SIZE_PX, SIZE_PX))
            image_path = AVATARS_PATH / f'{Path(urlparse(avatar_url).path).stem}.png'
            image.save(image_path, 'PNG')
            avatar_path = f'images/avatars/{image_path.name}'
        Member.create(id=member.id, avatar_path=avatar_path)

    week_ago = arrow.utcnow().shift(days=-1 * STATS_PERIOD_DAYS).naive

    authors = {}
    total_messages_count = Counter()
    week_messages_count = Counter()

    for channel in exclude_categories(client.juniorguru_guild.text_channels):
        log.info(f'#{channel.name}')
        async for message in channel.history(limit=None, after=None):
            authors.setdefault(message.author.id, message.author)
            total_messages_count[message.author.id] += 1
            if message.created_at > week_ago:
                week_messages_count[message.author.id] += 1

    for author_id in DEFAULT_EXCLUDED_MEMBERS:
        del total_messages_count[author_id]
        del week_messages_count[author_id]

    channel = await client.fetch_channel('moderátoři')
    await channel.send(
        '**Nejvíc příspěvků za celou dobu existence klubu**\n' +
        ''.join([f"{authors[author_id].mention} {count}\n"
                 for author_id, count in total_messages_count.most_common()[:5]]) +
        f'\n**Nejvíc příspěvků za posledních {STATS_PERIOD_DAYS} dní**\n' +
        ''.join([f"{authors[author_id].mention} {count}\n"
                 for author_id, count in week_messages_count.most_common()[:5]])
    )


def is_default_avatar(url):
    return bool(re.search(r'/embed/avatars/\d+\.', url))


if __name__ == '__main__':
    main()
