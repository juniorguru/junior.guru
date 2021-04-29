import math
from collections import Counter

from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, DISCORD_SENDING_ENABLED
from juniorguru.models import MessageAuthor, db


log = get_log('roles')


TOP_MEMBERS_PERCENT = 0.1

ROLE_MOST_MESSAGES = 836929320706113567
ROLE_MOST_HELPFUL = 836960665578766396
ROLE_HAS_INTRO = 836959652100702248
ROLE_HAS_IMAGE = 837016689505468436
ROLE_IS_NEW = 836930259982352435
ROLE_IS_SPONSOR = 837316268142493736


def main():
    with db:
        members = {member.id: member for member in MessageAuthor.members_listing()}
        display_name = create_display_name(members)
        members_count = len(members)
        top_members_limit = math.ceil(members_count * TOP_MEMBERS_PERCENT)
        log.info(f'members_count={members_count}, top_members_limit={top_members_limit}')

        messages_count = Counter({member.id: member.messages_count for member in members.values()})
        messages_count_stats = dict(messages_count.most_common()[:top_members_limit])
        log.info(f"messages_count: {repr_stats(messages_count_stats, display_name)}")

        recent_messages_count = Counter({member.id: member.recent_messages_count for member in members.values()})
        recent_messages_count_stats = dict(recent_messages_count.most_common()[:top_members_limit])
        log.info(f"recent_messages_count: {repr_stats(recent_messages_count_stats, display_name)}")

    most_discussing_members = set(messages_count_stats.keys()) | set(recent_messages_count_stats.keys())
    log.info(f"most_discussing_members: {', '.join(map(display_name, most_discussing_members))}")
    reassign_role(most_discussing_members, ROLE_MOST_MESSAGES)


@discord_task
async def reassign_role(client, members_ids, role_id):
    if DISCORD_SENDING_ENABLED:
        members_ids = set(members_ids)
        current_members = MessageAuthor.members_role_listing(role_id)
        current_members_ids = {member.id for member in current_members}

        members_ids_to_remove = current_members_ids - members_ids
        members_ids_to_add = members_ids - current_members_ids

        role = {role.id: role for role in await client.juniorguru_guild.fetch_roles()}[role_id]
        for member_id in members_ids_to_remove:
            member = await client.juniorguru_guild.fetch_member(member_id)
            await member.remove_roles(role)
        for member_id in members_ids_to_add:
            member = await client.juniorguru_guild.fetch_member(member_id)
            await member.add_roles(role)


def create_display_name(members):
    def display_name(member_id):
        return members[member_id].display_name
    return display_name


def repr_stats(stats, display_name):
    return ', '.join([f"{display_name(member_id)}={count}"
                      for member_id, count in stats.items()])


if __name__ == '__main__':
    main()
