from datetime import date, timedelta

from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, count_upvotes, is_default_avatar, get_roles, is_default_message_type, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import Message, MessageAuthor, db


log = get_log('messages')


EXCLUDE_CATEGORIES = [
    806097273536512010,  # CoreSkill's internal mentoring channels
]
META_CHANNEL = 797107515186741248 #806215364379148348


@discord_task
async def main(client):
    with db:
        db.drop_tables([Message, MessageAuthor])
        db.create_tables([Message, MessageAuthor])

    authors = {}
    channels = (channel for channel in client.juniorguru_guild.text_channels
                if not channel.category or channel.category.id not in EXCLUDE_CATEGORIES)
    for channel in channels:
        log.info(f'#{channel.name}')
        async for message in channel.history(limit=None, after=None):
            if message.author.id not in authors:
                # The message.author can be an instance of Member, but it can also be an instance of User,
                # if the author isn't a member of the Discord guild/server anymore. User instances don't
                # have certain properties, hence the getattr() calls below.
                with db:
                    author = MessageAuthor.create(id=message.author.id,
                                                  is_bot=message.author.bot,
                                                  is_member=bool(getattr(message.author, 'joined_at', False)),
                                                  has_avatar=not is_default_avatar(message.author.avatar_url),
                                                  display_name=message.author.display_name,
                                                  mention=message.author.mention,
                                                  joined_at=getattr(message.author, 'joined_at', None),
                                                  roles=get_roles(message.author))
                authors[message.author.id] = author
            with db:
                Message.create(id=message.id,
                               url=message.jump_url,
                               content=message.content,
                               upvotes=count_upvotes(message.reactions),
                               created_at=message.created_at,
                               edited_at=message.edited_at,
                               author=authors[message.author.id],
                               channel_id=channel.id,
                               channel_name=channel.name,
                               is_system=not is_default_message_type(message.type))

    with db:
        messages_count = Message.count()
    log.info(f'Saved {messages_count} messages from {len(authors)} authors')

    channel = await client.fetch_channel(META_CHANNEL)
    with db:
        digest = repr_digest(Message.digest_listing(date.today() - timedelta(weeks=1)))
    log.info(f'Sending digest: {repr(digest)}')
    if DISCORD_MUTATIONS_ENABLED:
        await channel.send(digest)


def repr_digest(messages):
    messages = list(messages)
    return '\n'.join([
        "🔥 Nejpopulárnější příspěvky za uplynulý týden 🔥",
        "",
        f"🥇 {messages[0].author.mention} {messages[0].url}",
        f"🥈 {messages[1].author.mention} {messages[1].url}",
        f"🥉 {messages[2].author.mention} {messages[2].url}",
    ])


if __name__ == '__main__':
    main()
