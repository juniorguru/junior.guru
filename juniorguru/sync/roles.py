from collections import Counter

from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task, DISCORD_MUTATIONS_ENABLED, get_roles
from juniorguru.models import ClubUser, Event, db


log = get_log('roles')


ROLE_MOST_DISCUSSING = 836929320706113567
ROLE_MOST_HELPFUL = 836960665578766396
ROLE_IS_SPEAKER = 836928169092710441
ROLE_HAS_INTRO_AND_AVATAR = 836959652100702248
ROLE_IS_NEW = 836930259982352435
ROLE_IS_SPONSOR = 837316268142493736  # TODO


def main():
    with db:
        members = ClubUser.members_listing()
        changes = []
        top_members_limit = ClubUser.top_members_limit()
        log.info(f'members_count={len(members)}, top_members_limit={top_members_limit}')

        # ROLE_MOST_DISCUSSING
        messages_count_stats = calc_stats(members, lambda m: m.messages_count(), top_members_limit)
        log.info(f"messages_count {repr_stats(members, messages_count_stats)}")

        recent_messages_count_stats = calc_stats(members, lambda m: m.recent_messages_count(), top_members_limit)
        log.info(f"recent_messages_count {repr_stats(members, recent_messages_count_stats)}")

        most_discussing_members_ids = set(messages_count_stats.keys()) | set(recent_messages_count_stats.keys())
        log.info(f"most_discussing_members: {repr_ids(members, most_discussing_members_ids)}")

        for member in members:
            changes.extend(evaluate_changes(member.id, member.roles, most_discussing_members_ids, ROLE_MOST_DISCUSSING))

        # ROLE_MOST_HELPFUL
        upvotes_count_stats = calc_stats(members, lambda m: m.upvotes_count(), top_members_limit)
        log.info(f"upvotes_count {repr_stats(members, upvotes_count_stats)}")

        recent_upvotes_count_stats = calc_stats(members, lambda m: m.recent_upvotes_count(), top_members_limit)
        log.info(f"recent_upvotes_count {repr_stats(members, recent_upvotes_count_stats)}")

        most_helpful_members_ids = set(upvotes_count_stats.keys()) | set(recent_upvotes_count_stats.keys())
        log.info(f"most_helpful_members: {repr_ids(members, most_helpful_members_ids)}")

        for member in members:
            changes.extend(evaluate_changes(member.id, member.roles, most_helpful_members_ids, ROLE_MOST_HELPFUL))

        # ROLE_HAS_INTRO_AND_AVATAR
        intro_avatar_members_ids = [member.id for member in members if member.has_avatar and member.has_intro()]
        log.info(f"intro_avatar_members: {repr_ids(members, intro_avatar_members_ids)}")
        for member in members:
            changes.extend(evaluate_changes(member.id, member.roles, intro_avatar_members_ids, ROLE_HAS_INTRO_AND_AVATAR))

        # ROLE_IS_NEW
        new_members_ids = [member.id for member in members if member.is_new()]
        log.info(f"new_members_ids: {repr_ids(members, new_members_ids)}")
        for member in members:
            changes.extend(evaluate_changes(member.id, member.roles, new_members_ids, ROLE_IS_NEW))

        # ROLE_IS_SPEAKER
        speaking_members_ids = [member.id for member in Event.list_speaking_members()]
        log.info(f"speaking_members_ids: {repr_ids(members, speaking_members_ids)}")
        for member in members:
            changes.extend(evaluate_changes(member.id, member.roles, speaking_members_ids, ROLE_IS_SPEAKER))

    if DISCORD_MUTATIONS_ENABLED:
        apply_changes(changes)
    else:
        log.warning("Skipping Discord mutations, DISCORD_MUTATIONS_ENABLED not set")


@discord_task
async def apply_changes(client, changes):
    all_discord_roles = {discord_role.id: discord_role
                         for discord_role in await client.juniorguru_guild.fetch_roles()}

    changes_by_members = {}
    for member_id, op, role_id in changes:
        changes_by_members.setdefault(member_id, dict(add=[], remove=[]))
        changes_by_members[member_id][op].append(role_id)

    for member_id, changes in changes_by_members.items():
        discord_member = await client.juniorguru_guild.fetch_member(member_id)
        if changes['add']:
            discord_roles = [all_discord_roles[role_id] for role_id in changes['add']]
            log.info(f'{discord_member.display_name}: adding {repr_roles(discord_roles)}')
            await discord_member.add_roles(*discord_roles)
        if changes['remove']:
            discord_roles = [all_discord_roles[role_id] for role_id in changes['remove']]
            log.info(f'{discord_member.display_name}: removing {repr_roles(discord_roles)}')
            await discord_member.remove_roles(*discord_roles)
        with db:
            member = ClubUser.get_by_id(member_id)
            member.roles = get_roles(discord_member)
            member.save()


def calc_stats(members, calc_member_fn, top_members_limit):
    counter = Counter({member.id: calc_member_fn(member) for member in members})
    return dict(counter.most_common()[:top_members_limit])


def evaluate_changes(member_id, current_roles_ids, role_members_ids, role_id):
    if member_id in role_members_ids and role_id not in current_roles_ids:
        return [(member_id, 'add', role_id)]
    if member_id not in role_members_ids and role_id in current_roles_ids:
        return [(member_id, 'remove', role_id)]
    return []


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
