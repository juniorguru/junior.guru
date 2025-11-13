import itertools
from collections import Counter
from pathlib import Path
from pprint import pformat
from typing import Iterable

import yaml
from discord import Color, Role
from pydantic import BaseModel

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.discord_club import ClubClient, get_user_roles, resolve_references
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate
from jg.coop.models.club import ClubUser
from jg.coop.models.event import Event
from jg.coop.models.partner import Partner
from jg.coop.models.role import DocumentedRole, InterestRole
from jg.coop.models.sponsor import Sponsor


IMAGES_DIR = Path("src/jg/coop/images")

YAML_PATH = Path("src/jg/coop/data/roles.yml")

INTEREST_ROLE_PREFIX = "Zajímá mě: "

ORG_ROLE_PREFIXES = {Sponsor: "Sponzor: ", Partner: "Partner: "}


logger = loggers.from_path(__file__)


class RoleConfig(BaseModel):
    id: int
    slug: str
    description: str


class FounderConfig(BaseModel):
    id: int
    account_id: int


class RolesConfig(BaseModel):
    registry: list[RoleConfig]
    founders: list[FounderConfig]


@cli.sync_command(
    dependencies=[
        "avatars",
        "candidates",
        "club-content",
        "events",
        "members",
        "organizations",
    ]
)
def main():
    discord_task.run(sync_roles)


@db.connection_context()
async def sync_roles(client: ClubClient):
    logger.info("Setting up db table for documented roles")
    db.drop_tables([DocumentedRole, InterestRole])
    db.create_tables([DocumentedRole, InterestRole])

    logger.info("Fetching info about roles")
    roles_config = RolesConfig(**yaml.safe_load(YAML_PATH.read_text()))
    roles_config_registry = {role.id: role for role in roles_config.registry}
    discord_roles = await client.club_guild.fetch_roles()
    documented_discord_roles = [
        discord_role
        for discord_role in discord_roles
        if discord_role.id in roles_config_registry
    ]

    # Why sorting and enumeration? Citing docs: "The recommended and correct way
    # to compare for roles in the hierarchy is using the comparison operators on
    # the role objects themselves."
    documented_discord_roles = sorted(documented_discord_roles, reverse=True)
    for position, discord_role in enumerate(documented_discord_roles, start=1):
        logger.debug(f"#{position} {discord_role.name}")
        DocumentedRole.create(
            club_id=discord_role.id,
            position=position,
            name=discord_role.name,
            mention=discord_role.mention,
            slug=roles_config_registry[discord_role.id].slug,
            description=resolve_references(
                roles_config_registry[discord_role.id].description.strip()
            ),
            emoji=discord_role.unicode_emoji,
            color=discord_role.color.value,
            icon_path=resolve_icon_path(discord_role),
        )

    for discord_role in discord_roles:
        if discord_role.name.startswith(INTEREST_ROLE_PREFIX):
            logger.debug(f"Interest role: {discord_role.name}")
            InterestRole.create(
                club_id=discord_role.id,
                name=discord_role.name,
                interest_name=discord_role.name.removeprefix(INTEREST_ROLE_PREFIX),
            )
    logger.info(f"Created {InterestRole.count()} interest roles")

    logger.info("Preparing data for computing how to re-assign roles")
    members = ClubUser.members_listing()
    organizations = list(itertools.chain(Sponsor.listing(), Partner.listing()))
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

    logger.info("Computing how to re-assign role: candidate")
    role_id = DocumentedRole.get_by_slug("candidate").club_id
    candidate_members = filter(
        None, [candidate.user for candidate in Candidate.listing()]
    )
    candidate_members_ids = [member.id for member in candidate_members]
    logger.debug(f"candidate_members: {repr_ids(members, candidate_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, candidate_members_ids, role_id
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

    logger.info("Computing how to re-assign role: founder")
    role_id = DocumentedRole.get_by_slug("founder").club_id
    founders_members_ids = [founder.id for founder in roles_config.founders]
    logger.debug(f"founders_members_ids: {repr_ids(members, founders_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, founders_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: sponsor")
    role_id = DocumentedRole.get_by_slug("sponsor").club_id
    sponsors_members_ids = [
        member.id
        for member in itertools.chain.from_iterable(
            sponsor.list_members for sponsor in Sponsor.listing()
        )
    ]
    logger.debug(f"sponsors_members_ids: {repr_ids(members, sponsors_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, sponsors_members_ids, role_id
            )
        )

    logger.info("Computing how to re-assign role: partner")
    role_id = DocumentedRole.get_by_slug("partner").club_id
    partners_members_ids = [
        member.id
        for member in itertools.chain.from_iterable(
            partner.list_members for partner in Partner.listing()
        )
    ]
    logger.debug(f"partners_members_ids: {repr_ids(members, partners_members_ids)}")
    for member in members:
        changes.extend(
            evaluate_changes(
                member.id, member.initial_roles, partners_members_ids, role_id
            )
        )

    # syncing with Discord
    logger.info(f"Managing roles for {len(organizations)} organizations")
    await manage_organization_roles(client, discord_roles, organizations)

    for org in organizations:
        org_members_ids = set(member.id for member in org.list_members)
        logger.debug(f"{org.slug}_members_ids: {repr_ids(members, org_members_ids)}")
        for member in members:
            changes.extend(
                evaluate_changes(
                    member.id, member.initial_roles, org_members_ids, org.role_id
                )
            )

    logger.info(f"Applying {len(changes)} changes to roles:\n{pformat(changes)}")
    await apply_changes(client, changes)


# TODO rewrite so it doesn't need any async/await and can be tested
async def manage_organization_roles(
    client: ClubClient, discord_roles, organizations: Iterable[Sponsor | Partner]
):
    org_roles_mapping = {
        f"{ORG_ROLE_PREFIXES[type(org)]}{org.name}": org for org in organizations
    }
    roles_names = list(org_roles_mapping.keys())
    roles_prefixes = tuple(ORG_ROLE_PREFIXES.values())
    logger.info(f"There should be {len(roles_names)} roles with organization prefixes")

    existing_roles = [
        role for role in discord_roles if role.name.startswith(roles_prefixes)
    ]
    logger.info(f"Found {len(existing_roles)} roles with organization prefixes")

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
            if role_name.startswith(roles_prefixes)
            else Color.default()
        )
        with mutating_discord(client.club_guild) as proxy:
            await proxy.create_role(name=role_name, color=color, mentionable=True)

    existing_roles = [
        role for role in discord_roles if role.name.startswith(roles_prefixes)
    ]
    for role in existing_roles:
        if org := org_roles_mapping.get(role.name):
            logger.info(f"Setting {role.name!r} to be organization role of {org!r}'")
            org.role_id = role.id
            org.save()


async def apply_changes(client: ClubClient, changes):
    # Can't take discord_roles as an argument and use instead of fetching, because before
    # this function runs, manage_sponsor_roles makes changes to the list of roles. This
    # function applies all changes to members, including the sponsor ones.
    all_discord_roles = {
        discord_role.id: discord_role
        for discord_role in await client.club_guild.fetch_roles()
    }

    changes_by_members = {}
    for member_id, op, role_id in changes:
        if role_id is None:
            logger.error(f"Cannot {op} role for #{member_id}: role_id not created yet")
        else:
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


def resolve_icon_path(role: Role | None) -> str | None:
    if role.icon:
        icon_path = IMAGES_DIR / "roles" / f"{role.id}.png"
        if not icon_path.exists():
            raise ValueError(
                f"Missing icon file: {icon_path} (download at {role.icon.url})"
            )
        return str(icon_path.relative_to(IMAGES_DIR))
    return None
