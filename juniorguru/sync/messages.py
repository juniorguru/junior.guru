import textwrap
from datetime import datetime, timedelta

from discord import Embed

from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, count_upvotes, is_default_avatar, get_roles, is_default_message_type, DISCORD_MUTATIONS_ENABLED
from juniorguru.models import Message, MessageAuthor, db


log = get_log('messages')


DIGEST_CHANNEL = 789046675247333397
DIGEST_LIMIT = 5


@discord_task
async def main(client):
    # MESSAGES AND AUTHORS
    with db:
        db.drop_tables([Message, MessageAuthor])
        db.create_tables([Message, MessageAuthor])

    authors = {}
    relevant_channels = (channel for channel in client.juniorguru_guild.text_channels
                         if channel.permissions_for(client.juniorguru_guild.me).read_messages)
    for channel in relevant_channels:
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
                               channel_mention=channel.mention,
                               is_system=not is_default_message_type(message.type))

    with db:
        messages_count = Message.count()
    log.info(f'Saved {messages_count} messages from {len(authors)} authors')

    # DIGEST
    week_ago_dt = datetime.utcnow() - timedelta(weeks=1)
    with db:
        last_digest_message = Message.last_bot_message(DIGEST_CHANNEL, '🔥')
    if last_digest_message:
        since_dt = last_digest_message.created_at
        log.info(f"Last digest on {since_dt}")
        if since_dt.date() > week_ago_dt.date():
            log.info(f"Aborting, {since_dt.date()} (last digest) > {week_ago_dt.date()} (week ago)")
            return  # abort
        else:
            log.info(f"About to create digest, {since_dt.date()} (last digest) <= {week_ago_dt.date()} (week ago)")
    else:
        since_dt = week_ago_dt
        log.info(f"Last digest not found, analyzing since {week_ago_dt}")

    channel = await client.fetch_channel(DIGEST_CHANNEL)
    with db:
        messages = Message.digest_listing(since_dt, limit=DIGEST_LIMIT)

    for n, message in enumerate(messages, start=1):
        log.info(f"Digest #{n}: {message.upvotes} votes for {message.author.display_name} in #{message.channel_name}, {message.url}")
    if DISCORD_MUTATIONS_ENABLED:
        content = [
            f"🔥 **{DIGEST_LIMIT} nej příspěvků za uplynulý týden (od {since_dt.day}.{since_dt.month}.)**",
            "",
            "Pokud je něco zajímavé nebo ti to pomohlo, dej tomu palec 👍, srdíčko ❤️, očička 👀, apod. Oceníš autory a pomůžeš tomu, aby se příspěvek mohl objevit i tady. Někomu, kdo nemá čas procházet všechno, co se v klubu napíše, se může tento přehled hodit.",
        ]
        embed_description = []
        for message in messages:
            embed_description += [
                f"{message.upvotes}× láska pro {message.author.mention} v {message.channel_mention}:",
                f"> {textwrap.shorten(message.content, 200, placeholder='…')}",
                f"[Hop na příspěvek]({message.url})",
                "",
            ]
        await channel.send(content="\n".join(content),
                           embed=Embed(description="\n".join(embed_description)))
    else:
        log.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


if __name__ == '__main__':
    main()
