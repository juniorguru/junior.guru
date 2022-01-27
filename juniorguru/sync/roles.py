from collections import Counter

from discord import Colour

from juniorguru.models.company import Company
from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import discord_task, is_discord_mutable, get_roles
from juniorguru.models import ClubUser, Event, with_db


logger = loggers.get('roles')


ROLES = {
    'most_discussing': 836929320706113567,
    'most_helpful': 836960665578766396,
    'is_speaker': 836928169092710441,
    'has_intro_and_avatar': 836959652100702248,
    'is_new': 836930259982352435,
    'is_sponsor': 837316268142493736,
    'is_founder': 917431428227145780,
    'is_year_old': 917430017993093140,
}


@measure('roles')
@with_db
def main():
    members = ClubUser.members_listing()
    companies = Company.listing()
    changes = []
    top_members_limit = ClubUser.top_members_limit()
    logger.info(f'members_count={len(members)}, top_members_limit={top_members_limit}')

    # role 'most_discussing'
    messages_count_stats = calc_stats(members, lambda m: m.messages_count(), top_members_limit)
    logger.debug(f"messages_count {repr_stats(members, messages_count_stats)}")

    recent_messages_count_stats = calc_stats(members, lambda m: m.recent_messages_count(), top_members_limit)
    logger.debug(f"recent_messages_count {repr_stats(members, recent_messages_count_stats)}")

    most_discussing_members_ids = set(messages_count_stats.keys()) | set(recent_messages_count_stats.keys())
    logger.debug(f"most_discussing_members: {repr_ids(members, most_discussing_members_ids)}")

    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, most_discussing_members_ids, ROLES['most_discussing']))

    # role 'most_helpful'
    upvotes_count_stats = calc_stats(members, lambda m: m.upvotes_count(), top_members_limit)
    logger.debug(f"upvotes_count {repr_stats(members, upvotes_count_stats)}")

    recent_upvotes_count_stats = calc_stats(members, lambda m: m.recent_upvotes_count(), top_members_limit)
    logger.debug(f"recent_upvotes_count {repr_stats(members, recent_upvotes_count_stats)}")

    most_helpful_members_ids = set(upvotes_count_stats.keys()) | set(recent_upvotes_count_stats.keys())
    logger.debug(f"most_helpful_members: {repr_ids(members, most_helpful_members_ids)}")

    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, most_helpful_members_ids, ROLES['most_helpful']))

    # role 'has_intro_and_avatar'
    intro_avatar_members_ids = [member.id for member in members if member.avatar_path and member.has_intro()]
    logger.debug(f"intro_avatar_members: {repr_ids(members, intro_avatar_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, intro_avatar_members_ids, ROLES['has_intro_and_avatar']))

    # role 'is_new'
    new_members_ids = [member.id for member in members if member.is_new()]
    logger.debug(f"new_members_ids: {repr_ids(members, new_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, new_members_ids, ROLES['is_new']))

    # role 'is_year_old'
    year_old_members_ids = [member.id for member in members if member.is_year_old()]
    logger.debug(f"year_old_members_ids: {repr_ids(members, year_old_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, year_old_members_ids, ROLES['is_year_old']))

    # role 'is_speaker'
    speaking_members_ids = [member.id for member in Event.list_speaking_members()]
    logger.debug(f"speaking_members_ids: {repr_ids(members, speaking_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, speaking_members_ids, ROLES['is_speaker']))

    # role 'is_founder'
    founders_members_ids = [member.id for member in members if member.is_founder()]
    logger.debug(f"founders_members_ids: {repr_ids(members, founders_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, founders_members_ids, ROLES['is_founder']))

    # role 'is_sponsor'
    coupons = list(filter(None, (company.coupon for company in companies)))
    sponsoring_members_ids = [member.id for member in members if member.coupon in coupons]
    logger.debug(f"sponsoring_members_ids: {repr_ids(members, sponsoring_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, sponsoring_members_ids, ROLES['is_sponsor']))

    # syncing with Discord
    if is_discord_mutable():
        sync_roles(changes, companies)


@discord_task
async def sync_roles(client, changes, companies):
    logger.info(f'Creating roles for {len(companies)} companies')
    await create_company_roles(client, companies)
    for company in companies:
        changes.extend([(member.id, 'add', company.role_id)
                        for member in company.list_employees])
        changes.extend([(member.id, 'add', company.student_role_id)
                        for member in company.list_students])

    logger.info(f'Applying {len(changes)} changes to roles')
    await apply_changes(client, changes)


async def create_company_roles(client, companies):
    for role in (await client.juniorguru_guild.fetch_roles()):
        if role.name.startswith(('Firma:', 'Student:')):
            logger.debug(f"Removing role '{role.name}'")
            await role.delete()

    for company in companies:
        role = await client.juniorguru_guild.create_role(
            name=f'Firma: {company.name}',
            colour=Colour.dark_grey(),
            mentionable=True,
        )
        logger.debug(f"Created role '{role.name}'")
        company.role_id = role.id

        if company.student_coupon:
            student_role = await client.juniorguru_guild.create_role(
                name=f'Student: {company.name}',
                mentionable=True,
            )
            logger.debug(f"Created role '{student_role.name}'")
            company.student_role_id = student_role.id

        company.save()


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
            logger.info(f'{discord_member.display_name}: adding {repr_roles(discord_roles)}')
            await discord_member.add_roles(*discord_roles)
        if changes['remove']:
            discord_roles = [all_discord_roles[role_id] for role_id in changes['remove']]
            logger.info(f'{discord_member.display_name}: removing {repr_roles(discord_roles)}')
            await discord_member.remove_roles(*discord_roles)

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
