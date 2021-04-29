from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, exclude_categories, count_downvotes, count_upvotes
from juniorguru.models import Message, MessageAuthor, db


log = get_log('messages')


@discord_task
async def main(client):
    with db:
        db.drop_tables([Message, MessageAuthor])
        db.create_tables([Message, MessageAuthor])

    authors = {}
    for channel in exclude_categories(client.juniorguru_guild.text_channels):
        log.info(f'#{channel.name}')
        async for message in channel.history(limit=None, after=None):
            if message.author.id not in authors:
                # The message.author can be an instance of Member, but it can also be an instance of User,
                # if the author isn't a member of the Discord guild/server anymore. User instances don't
                # have certain properties, hence the getattr() calls below.
                with db:
                    roles = [role.id for role in getattr(message.author, 'roles', [])]
                    author = MessageAuthor.create(id=message.author.id,
                                                  is_bot=message.author.bot,
                                                  is_member=bool(getattr(message.author, 'joined_at', False)),
                                                  display_name=message.author.display_name,
                                                  roles=roles)
                authors[message.author.id] = author
            with db:
                Message.create(id=message.id,
                               content=message.content,
                               upvotes=count_upvotes(message.reactions),
                               downvotes=count_downvotes(message.reactions),
                               created_at=message.created_at,
                               edited_at=message.edited_at,
                               author=authors[message.author.id],
                               channel_id=channel.id,
                               channel_name=channel.name)

    with db:
        messages_count = Message.count()
        authors_count = MessageAuthor.count()
    assert authors_count == len(authors)
    log.info(f'Saved {messages_count} messages from {authors_count} authors')

    with db:
        for author in authors.values():
            log.info(f'Calculating stats for {author.display_name}')
            author.calc_messages_count()
            author.calc_recent_messages_count()
            author.save()


if __name__ == '__main__':
    main()
