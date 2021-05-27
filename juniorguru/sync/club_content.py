from juniorguru.lib.log import get_log
from juniorguru.lib.club import EMOJI_PINS, discord_task, count_upvotes, emoji_name, get_roles, count_pins
from juniorguru.models import ClubMessage, ClubUser, ClubPinReaction, db


log = get_log('club_content')


@discord_task
async def main(client):
    with db:
        db.drop_tables([ClubMessage, ClubUser, ClubPinReaction])
        db.create_tables([ClubMessage, ClubUser, ClubPinReaction])

    authors = {}
    relevant_channels = (channel for channel in client.juniorguru_guild.text_channels
                         if channel.permissions_for(client.juniorguru_guild.me).read_messages)
    for channel in relevant_channels:
        log.info(f'Channel #{channel.name}')
        async for message in channel.history(limit=None, after=None):
            if message.author.id not in authors:
                # The message.author can be an instance of Member, but it can also be an instance of User,
                # if the author isn't a member of the Discord guild/server anymore. User instances don't
                # have certain properties, hence the getattr() calls below.
                with db:
                    log.info(f"User '{message.author.display_name}' #{message.author.id}")
                    author = ClubUser.create(id=message.author.id,
                                             is_bot=message.author.bot,
                                             is_member=bool(getattr(message.author, 'joined_at', False)),
                                             display_name=message.author.display_name,
                                             mention=message.author.mention,
                                             joined_at=getattr(message.author, 'joined_at', None),
                                             roles=get_roles(message.author))
                authors[message.author.id] = author
            with db:
                ClubMessage.create(id=message.id,
                                   url=message.jump_url,
                                   content=message.content,
                                   upvotes_count=count_upvotes(message.reactions),
                                   pin_reactions_count=count_pins(message.reactions),
                                   created_at=message.created_at,
                                   edited_at=message.edited_at,
                                   author=authors[message.author.id],
                                   channel_id=channel.id,
                                   channel_name=channel.name,
                                   channel_mention=channel.mention,
                                   type=message.type.name)

                users = set()
                for reaction in message.reactions:
                    if emoji_name(reaction.emoji) in EMOJI_PINS:
                        for user in [user async for user in reaction.users()]:
                            users.add(user)
                for user in users:
                    ClubPinReaction.create(user=user.id, message=message.id)

    # remaining members (did not author a single message)
    log.info('Looking for remaining members, if any')
    remaining_members = [member async for member in client.juniorguru_guild.fetch_members(limit=None)
                         if member.id not in authors]
    for member in remaining_members:
        with db:
            log.info(f"Member '{member.display_name}' #{member.id}")
            ClubUser.create(id=member.id,
                            is_bot=member.bot,
                            is_member=True,
                            display_name=member.display_name,
                            mention=member.mention,
                            joined_at=member.joined_at,
                            roles=get_roles(member))

    with db:
        messages_count = ClubMessage.count()
        members_count = ClubUser.members_count()
    log.info(f'Saved {messages_count} messages from {len(authors)} authors')
    log.info(f'Saved {members_count} members')


if __name__ == '__main__':
    main()
