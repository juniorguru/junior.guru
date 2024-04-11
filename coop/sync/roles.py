from collections import Counter
from pathlib import Path
from pprint import pformat

import emoji
from discord import Color
from slugify import slugify
from strictyaml import Int, Map, Seq, Str, load

from coop.cli.sync import main as cli
from coop.lib import discord_task, loggers
from coop.lib.discord_club import ClubClient, get_user_roles, resolve_references
from coop.lib.mutations import mutating_discord
from coop.models.base import db
from coop.models.club import ClubUser
from coop.models.documented_role import DocumentedRole
from coop.models.event import Event
from coop.models.mentor import Mentor
from coop.models.partner import Partnership


IMAGES_DIR = Path("coop/images")

YAML_PATH = Path("coop/data/roles.yml")

YAML_SCHEMA = Seq(
    Map(
        {
            "id": Int(),
            "slug": Str(),
            "description": Str(),
        }
    )
)

PARTNER_ROLE_PREFIX = "Firma: "


logger = loggers.from_path(__file__)


@cli.sync_command(
    dependencies=[
        "club-content",
        "events",
        "avatars",
        "members",
        "partners",
        "mentoring",
    ]
)
def main():
    discord_task.run(sync_roles)


@db.connection_context()
async def sync_roles(client: ClubClient):
    logger.info("Setting up db table for documented roles")
    DocumentedRole.drop_table()
    DocumentedRole.create_table()

    logger.info("Fetching info about roles")
    yaml_records = {
        record.data["id"]: record.data
        for record in load(YAML_PATH.read_text(), YAML_SCHEMA)
    }
    discord_roles = await client.club_guild.fetch_roles()
    documented_discord_roles = [
        discord_role
        for discord_role in discord_roles
        if discord_role.id in yaml_records
    ]

    # Why sorting and enumeration? Citing docs: "The recommended and correct way
    # to compare for roles in the hierarchy is using the comparison operators on
    # the role objects themselves."
    documented_discord_roles = sorted(
        documented_discord_roles,
        reverse=True,
    )
    for position, discord_role in enumerate(documented_discord_roles, start=1):
        logger.debug(f"#{position} {discord_role.name}")

        if discord_role.icon:
            icon_path = IMAGES_DIR / "emoji" / f"club-role-{discord_role.id}.png"
            if not icon_path.exists():
                raise ValueError(
                    f"Missing icon file: {icon_path} (download at {discord_role.icon.url})"
                )
        elif discord_role.unicode_emoji:
            icon_path = (
                IMAGES_DIR / "emoji" / f"{emoji_slug(discord_role.unicode_emoji)}.png"
            )
            if not icon_path.exists():
                raise ValueError(
                    f"Missing icon file: {icon_path} (download at https://emojipedia.org/twitter/twemoji-15.0.1/{emoji_slug(discord_role.unicode_emoji)})"
                )
        else:
            icon_path = None

        DocumentedRole.create(
            club_id=discord_role.id,
            position=position,
            name=discord_role.name,
            mention=discord_role.mention,
            slug=yaml_records[discord_role.id]["slug"],
            description=resolve_references(
                yaml_records[discord_role.id]["description"].strip()
            ),
            emoji=discord_role.unicode_emoji,
            color=discord_role.color.value,
            icon_path=icon_path.relative_to(IMAGES_DIR) if icon_path else None,
        )

    logger.info("Preparing data for computing how to re-assign roles")
    members = ClubUser.members_listing()
    partners = [partnership.partner for partnership in Partnership.active_listing()]
    changes = []
    top_members_limit = ClubUser.top_members_limit()
    logger.info(f"members_count={len(members)}, top_members_limit={top_members_limit}")

    logger.info("Computing how to re-assign role: most_discussing")
    role_id = DocumentedRole.get_by_slug("most_discussing").club_id
    content_size_stats = calc_stats(
        members, lambda m: m.content_size(), top_members_limit
    )
    logger.debug(f"content_size {repr_stats(members, content_size_stats)}")
    recent_content_size_stats = calc_stats(
        members, lambda m: m.recent_content_size(), top_members_limit
    )
    logger.debug(
        f"recent_content_size {repr_stats(members, recent_content_size_stats)}"
    )
    most_discussing_members_ids = set(content_size_stats.keys()) | set(
        recent_content_size_stats.keys()
    )
    logger.debug(
        f"most_discussing_members: {repr_ids(members, most_discussing_members_ids)}"
    )
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, most_discussing_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: most_helpful")
    role_id = DocumentedRole.get_by_slug("most_helpful").club_id
    upvotes_count_stats = calc_stats(
        members, lambda m: m.upvotes_count(), top_members_limit
    )
    logger.debug(f"upvotes_count {repr_stats(members, upvotes_count_stats)}")
    recent_upvotes_count_stats = calc_stats(
        members, lambda m: m.recent_upvotes_count(), top_members_limit
    )
    logger.debug(
        f"recent_upvotes_count {repr_stats(members, recent_upvotes_count_stats)}"
    )
    most_helpful_members_ids = set(upvotes_count_stats.keys()) | set(
        recent_upvotes_count_stats.keys()
    )
    logger.debug(f"most_helpful_members: {repr_ids(members, most_helpful_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, most_helpful_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: has_intro_and_avatar")
    role_id = DocumentedRole.get_by_slug("has_intro_and_avatar").club_id
    intro_avatar_members_ids = [
        member.id for member in members if member.has_avatar and member.intro
    ]
    logger.debug(f"intro_avatar_members: {repr_ids(members, intro_avatar_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, intro_avatar_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: newcomer")
    role_id = DocumentedRole.get_by_slug("newcomer").club_id
    new_members_ids = [member.id for member in members if member.is_new()]
    logger.debug(f"new_members_ids: {repr_ids(members, new_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(member.id, member.initial_roles, new_members_ids, role_id)
        )

    logger.info("Computing how to re-assign role: speaker")
    role_id = DocumentedRole.get_by_slug("speaker").club_id
    speaking_members_ids = [member.id for member in Event.list_speaking_members()]
    logger.debug(f"speaking_members_ids: {repr_ids(members, speaking_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, speaking_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: mentor")
    role_id = DocumentedRole.get_by_slug("mentor").club_id
    mentors_members_ids = [mentor.user.id for mentor in Mentor.listing()]
    logger.debug(f"mentors_ids: {repr_ids(members, mentors_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, mentors_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: founder")
    role_id = DocumentedRole.get_by_slug("founder").club_id
    founders_members_ids = [member.id for member in members if member.is_founder()]
    logger.debug(f"founders_members_ids: {repr_ids(members, founders_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, founders_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: partner")
    role_id = DocumentedRole.get_by_slug("partner").club_id
    coupons = list(filter(None, (partner.coupon for partner in partners)))
    partners_members_ids = [member.id for member in members if member.coupon in coupons]
    logger.debug(f"partners_members_ids: {repr_ids(members, partners_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, partners_members_ids, role_id
            )
        )

    # syncing with Discord
    logger.info(f"Managing roles for {len(partners)} partners")
    await manage_partner_roles(client, discord_roles, partners)

    for partner in partners:
        partner_members_ids = [member.id for member in partner.list_members]
        logger.debug(
            f"partner_members_ids({partner!r}): {repr_ids(members, partner_members_ids)}"
        )
        for member in members:
            changes.extend(
                evaluate_changes(
                    member.id,
                    member.initial_roles,
                    partner_members_ids,
                    partner.role_id,
                )
            )

    logger.info(f"Applying {len(changes)} changes to roles:\n{pformat(changes)}")
    await apply_changes(client, changes)


# TODO rewrite so it doesn't need any async/await and can be tested
async def manage_partner_roles(client: ClubClient, discord_roles, partners):
    partner_roles_mapping = {
        PARTNER_ROLE_PREFIX + partner.name: partner for partner in partners
    }
    roles_names = list(partner_roles_mapping.keys())
    logger.info(f"There should be {len(roles_names)} roles with partner prefixes")

    existing_roles = [
        role for role in discord_roles if role.name.startswith(PARTNER_ROLE_PREFIX)
    ]
    logger.info(f"Found {len(existing_roles)} roles with partner prefixes")

    roles_to_remove = [role for role in existing_roles if role.name not in roles_names]
    logger.info(
        f"Roles [{', '.join([role.name for role in roles_to_remove])}] will be removed"
    )
    for role in roles_to_remove:
        logger.info(f"Removing role '{role.name}'")
        with mutating_discord(role) as proxy:
            await proxy.delete()

    roles_names_to_add = set(roles_names) - {role.name for role in existing_roles}
    logger.info(f"Roles [{', '.join(roles_names_to_add)}] will be added")
    for role_name in roles_names_to_add:
        logger.info(f"Adding role '{role_name}'")
        color = (
            Color.dark_grey()
            if role_name.startswith(PARTNER_ROLE_PREFIX)
            else Color.default()
        )
        with mutating_discord(client.club_guild) as proxy:
            await proxy.create_role(name=role_name, color=color, mentionable=True)

    existing_roles = [
        role for role in discord_roles if role.name.startswith(PARTNER_ROLE_PREFIX)
    ]
    for role in existing_roles:
        partner = partner_roles_mapping.get(role.name)
        if partner:
            logger.info(f"Setting '{role.name}' to be employee role of {partner!r}'")
            partner.role_id = role.id
            partner.save()


async def apply_changes(client: ClubClient, changes):
    # Can't take discord_roles as an argument and use instead of fetching, because before
    # this function runs, manage_partner_roles makes changes to the list of roles. This
    # function applies all changes to members, including the partner ones.
    all_discord_roles = {
        discord_role.id: discord_role
        for discord_role in await client.club_guild.fetch_roles()
    }

    changes_by_members = {}
    for member_id, op, role_id in changes:
        changes_by_members.setdefault(member_id, dict(add=[], remove=[]))
        changes_by_members[member_id][op].append(role_id)

    for member_id, changes in changes_by_members.items():
        discord_member = await client.club_guild.fetch_member(member_id)
        if changes["add"]:
            discord_roles = [all_discord_roles[role_id] for role_id in changes["add"]]
            logger.debug(
                f"{discord_member.display_name}: adding {repr_roles(discord_roles)}"
            )
            with mutating_discord(discord_member) as proxy:
                await proxy.add_roles(*discord_roles)
        if changes["remove"]:
            discord_roles = [
                all_discord_roles[role_id] for role_id in changes["remove"]
            ]
            logger.debug(
                f"{discord_member.display_name}: removing {repr_roles(discord_roles)}"
            )
            with mutating_discord(discord_member) as proxy:
                await proxy.remove_roles(*discord_roles)

        member = ClubUser.get_by_id(member_id)
        member.updated_roles = get_user_roles(discord_member)
        member.save()


def calc_stats(members, calc_member_fn, top_members_limit):
    counter = Counter({member.id: calc_member_fn(member) for member in members})
    return dict(counter.most_common()[:top_members_limit])


def evaluate_changes(member_id, initial_roles_ids, role_members_ids, role_id):
    if member_id in role_members_ids and role_id not in initial_roles_ids:
        return [(member_id, "add", role_id)]
    if member_id not in role_members_ids and role_id in initial_roles_ids:
        return [(member_id, "remove", role_id)]
    return []


def repr_stats(members, stats):
    display_names = {member.id: member.display_name for member in members}
    return repr({display_names[member_id]: count for member_id, count in stats.items()})


def repr_ids(members, members_ids):
    display_names = {member.id: member.display_name for member in members}
    return repr(
        sorted(
            [
                display_names.get(member_id, "(doesn't exist)")
                for member_id in members_ids
            ],
            key=str.lower,
        )
    )


def repr_roles(roles):
    return repr([role.name for role in roles])


def emoji_slug(unicode_emoji: str) -> str:
    return slugify(emoji.demojize(unicode_emoji))
