from collections import Counter

from discord import Colour

from juniorguru.models.company import Company
from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, is_discord_mutable, get_roles
from juniorguru.models import ClubUser, Event, db


logger = loggers.get(__name__)


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
COMPANY_ROLE_PREFIX = 'Firma: '
STUDENT_ROLE_PREFIX = 'Student: '


@measure()
def main():
    run_discord_task('juniorguru.sync.stickers.discord_task')


@db.connection_context()
async def discord_task(client):
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
    coupons = list(filter(None, (company.coupon_base for company in companies)))
    sponsoring_members_ids = [member.id for member in members if member.coupon_base in coupons]
    logger.debug(f"sponsoring_members_ids: {repr_ids(members, sponsoring_members_ids)}")
    for member in members:
        changes.extend(evaluate_changes(member.id, member.roles, sponsoring_members_ids, ROLES['is_sponsor']))

    # syncing with Discord
    if is_discord_mutable():
        logger.info(f'Managing roles for {len(companies)} companies')
        await manage_company_roles(client, companies)

        for company in companies:
            employees_ids = [member.id for member in company.list_employees]
            logger.debug(f"employees_ids({company.name}): {repr_ids(members, employees_ids)}")
            for member in members:
                changes.extend(evaluate_changes(member.id, member.roles, employees_ids, company.role_id))

            students_ids = [member.id for member in company.list_students]
            logger.debug(f"students_ids({company.name}): {repr_ids(members, students_ids)}")
            for member in members:
                changes.extend(evaluate_changes(member.id, member.roles, students_ids, company.student_role_id))

        logger.info(f'Applying {len(changes)} changes to roles')
        await apply_changes(client, changes)


async def manage_company_roles(client, companies):
    company_roles_mapping = {COMPANY_ROLE_PREFIX + company.name: company
                             for company in companies}
    student_roles_mapping = {STUDENT_ROLE_PREFIX + company.name: company
                             for company in companies if company.student_coupon_base}
    roles_names = list(company_roles_mapping.keys()) + list(student_roles_mapping.keys())
    logger.info(f"There should be {len(roles_names)} roles with company or student prefixes")

    existing_roles = [role for role in (await client.juniorguru_guild.fetch_roles())
                      if role.name.startswith((COMPANY_ROLE_PREFIX, STUDENT_ROLE_PREFIX))]
    logger.info(f"Found {len(existing_roles)} roles with company or student prefixes")

    roles_to_remove = [role for role in existing_roles if role.name not in roles_names]
    logger.info(f"Roles [{', '.join([role.name for role in roles_to_remove])}] will be removed")
    for role in roles_to_remove:
        logger.info(f"Removing role '{role.name}'")
        await role.delete()

    roles_names_to_add = set(roles_names) - {role.name for role in existing_roles}
    logger.info(f"Roles [{', '.join(roles_names_to_add)}] will be added")
    for role_name in roles_names_to_add:
        logger.info(f"Adding role '{role_name}'")
        colour = Colour.dark_grey() if role_name.startswith(COMPANY_ROLE_PREFIX) else Colour.default()
        await client.juniorguru_guild.create_role(name=role_name, colour=colour, mentionable=True)

    existing_roles = [role for role in (await client.juniorguru_guild.fetch_roles())
                      if role.name.startswith((COMPANY_ROLE_PREFIX, STUDENT_ROLE_PREFIX))]
    for role in existing_roles:
        company = company_roles_mapping.get(role.name)
        if company:
            logger.info(f"Setting '{role.name}' to be employee role of '{company.name}'")
            company.role_id = role.id
            company.save()
        else:
            company = student_roles_mapping.get(role.name)
            if company:
                logger.info(f"Setting '{role.name}' to be student role of '{company.name}'")
                company.student_role_id = role.id
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
            logger.debug(f'{discord_member.display_name}: adding {repr_roles(discord_roles)}')
            await discord_member.add_roles(*discord_roles)
        if changes['remove']:
            discord_roles = [all_discord_roles[role_id] for role_id in changes['remove']]
            logger.debug(f'{discord_member.display_name}: removing {repr_roles(discord_roles)}')
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
