from collections import Counter

from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED, get_roles
from juniorguru.models import MessageAuthor, db


log = get_log('roles')


ROLE_MOST_DISCUSSING = 836929320706113567
ROLE_MOST_HELPFUL = 836960665578766396
ROLE_IS_SPEAKER = 836928169092710441  # TODO
ROLE_HAS_INTRO_AND_AVATAR = 836959652100702248
ROLE_IS_NEW = 836930259982352435
ROLE_IS_SPONSOR = 837316268142493736  # TODO


def main():
    with db:
        members = MessageAuthor.members_listing()
        top_members_limit = MessageAuthor.top_members_limit()
        log.info(f'members_count={MessageAuthor.count()}, top_members_limit={top_members_limit}')

        # ROLE_MOST_DISCUSSING
        messages_count_stats = calc_stats(members, 'messages_count', top_members_limit)
        log.info(f"messages_count {repr_stats(members, messages_count_stats)}")

        recent_messages_count_stats = calc_stats(members, 'recent_messages_count', top_members_limit)
        log.info(f"recent_messages_count {repr_stats(members, recent_messages_count_stats)}")

        most_discussing_members_ids = set(messages_count_stats.keys()) | set(recent_messages_count_stats.keys())
        log.info(f"most_discussing_members: {repr_ids(members, most_discussing_members_ids)}")

        for member in members:
            record_role_diff(member, most_discussing_members_ids, ROLE_MOST_DISCUSSING)
            member.save()

        # ROLE_MOST_HELPFUL
        upvotes_count_stats = calc_stats(members, 'upvotes_count', top_members_limit)
        log.info(f"upvotes_count {repr_stats(members, upvotes_count_stats)}")

        recent_upvotes_count_stats = calc_stats(members, 'recent_upvotes_count', top_members_limit)
        log.info(f"recent_upvotes_count {repr_stats(members, recent_upvotes_count_stats)}")

        most_helpful_members_ids = set(upvotes_count_stats.keys()) | set(recent_upvotes_count_stats.keys())
        log.info(f"most_helpful_members: {repr_ids(members, most_helpful_members_ids)}")

        for member in members:
            record_role_diff(member, most_helpful_members_ids, ROLE_MOST_HELPFUL)
            member.save()

        # ROLE_HAS_INTRO_AND_AVATAR
        intro_avatar_members_ids = [member.id for member in members if member.has_avatar and member.has_intro]
        log.info(f"intro_avatar_members: {repr_ids(members, intro_avatar_members_ids)}")
        for member in members:
            record_role_diff(member, intro_avatar_members_ids, ROLE_HAS_INTRO_AND_AVATAR)
            member.save()

        # ROLE_IS_NEW
        new_members_ids = [member.id for member in members if member.is_new()]
        log.info(f"new_members_ids: {repr_ids(members, new_members_ids)}")
        for member in members:
            record_role_diff(member, new_members_ids, ROLE_IS_NEW)
            member.save()

    if DISCORD_MUTATIONS_ENABLED:
        apply_role_diffs(members)


@discord_task
async def apply_role_diffs(client, members):
    all_discord_roles = {discord_role.id: discord_role
                         for discord_role in await client.juniorguru_guild.fetch_roles()}
    with db:
        for db_member in members:
            discord_member = await client.juniorguru_guild.fetch_member(db_member.id)
            try:
                if db_member.roles_add:
                    discord_roles = [all_discord_roles[role_id] for role_id in db_member.roles_add]
                    log.info(f'{discord_member.display_name}: adding {repr_roles(discord_roles)}')
                    await discord_member.add_roles(*discord_roles)
                if db_member.roles_remove:
                    discord_roles = [all_discord_roles[role_id] for role_id in db_member.roles_remove]
                    log.info(f'{discord_member.display_name}: removing {repr_roles(discord_roles)}')
                    await discord_member.remove_roles(*discord_roles)
            finally:
                db_member.roles_add = []
                db_member.roles_remove = []
                db_member.roles = get_roles(discord_member)
                db_member.save()


def calc_stats(members, prop, top_members_limit):
    counter = Counter({member.id: getattr(member, prop) for member in members})
    return dict(counter.most_common()[:top_members_limit])


def record_role_diff(member, members_ids, role_id):
    if member.id in members_ids and role_id not in member.roles:
        member.roles_add.append(role_id)
    if member.id not in members_ids and role_id in member.roles:
        member.roles_remove.append(role_id)


def repr_stats(members, stats):
    display_names = {member.id: member.display_name for member in members}
    return repr({display_names[member_id]: count for member_id, count in stats.items()})


def repr_ids(members, members_ids):
    display_names = {member.id: member.display_name for member in members}
    return repr([display_names[member_id] for member_id in members_ids])


def repr_roles(roles):
    return repr([role.name for role in roles])


if __name__ == '__main__':
    main()
