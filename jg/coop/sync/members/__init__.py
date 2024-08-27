import math
from collections import defaultdict
from datetime import date, datetime
from enum import StrEnum
from operator import itemgetter
from pathlib import Path
from pprint import pformat
from typing import DefaultDict, Iterable, Literal, TypedDict

import click
from discord import NotFound
from playhouse.shortcuts import model_to_dict

from jg.coop.cli.sync import main as cli
from jg.coop.lib import discord_task, loggers
from jg.coop.lib.coupons import parse_coupon
from jg.coop.lib.discord_club import ClubChannelID, ClubClient, ClubMemberID
from jg.coop.lib.memberful import (
    MemberfulAPI,
    is_group_plan,
    is_individual_plan,
    is_partner_plan,
    is_sponsor_plan,
    memberful_url,
    timestamp_to_date,
    timestamp_to_datetime,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubUser, SubscriptionType
from jg.coop.models.feminine_name import FeminineName
from jg.coop.models.members import Members


logger = loggers.from_path(__file__)


MEMBERS_GQL_PATH = Path(__file__).parent / "members.gql"


class MemberState(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class PlanEntity(TypedDict):
    name: str
    intervalUnit: Literal["week", "month", "year"]
    forSale: bool
    additionalMemberPriceCents: int | None
    planGroup: dict


class SubscriptionEntity(TypedDict):
    id: str
    active: bool
    activatedAt: int
    trialStartAt: int
    trialEndAt: int
    expiresAt: int
    coupon: dict  # TODO
    orders: list[dict]  # TODO
    plan: PlanEntity


class MemberEntity(TypedDict):
    id: str
    discordUserId: str
    email: str
    fullName: str
    totalSpendCents: int
    stripeCustomerId: str
    subscriptions: list[SubscriptionEntity]


StatName = Literal["quits", "signups", "trials"]


@cli.sync_command(dependencies=["club-content", "feminine-names", "subscriptions"])
@click.option(
    "--history-path",
    default="jg/coop/data/members.jsonl",
    type=click.Path(path_type=Path),
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
def main(history_path: Path, today: date):
    logger.info("Getting data from Memberful")
    memberful = MemberfulAPI()

    members: Iterable[MemberEntity] = memberful.get_nodes(MEMBERS_GQL_PATH.read_text())
    seen_discord_ids = set()

    stats_from = today.replace(day=1)
    stats_to = today
    stats: DefaultDict[StatName, int] = defaultdict(int)

    for member in logger.progress(members):
        account_id = int(member["id"])
        member_admin_url = memberful_url(account_id)

        logger.info(f"Processing member {member_admin_url}")
        if is_active(member["subscriptions"]):
            try:
                discord_id = int(member["discordUserId"])  # raies TypeError if None
                user = ClubUser.get_by_id(discord_id)  # raises ClubUser.DoesNotExist
            except (TypeError, ClubUser.DoesNotExist):
                logger.warning(f"Member {member_admin_url} isn't on Discord")
            else:
                logger.debug(f"Identified as club user #{user.id}")
                seen_discord_ids.add(user.id)

                name = member["fullName"].strip()
                has_feminine_name = FeminineName.is_feminine(name)

                subscription = get_active_subscription(member["subscriptions"])
                logger.debug(f"Subscription of {member_admin_url}: {subscription}")

                subscription_id = str(subscription["id"])
                coupon = get_coupon(subscription)
                coupon_parts = parse_coupon(coupon) if coupon else {}
                expires_at = get_expires_at(member["subscriptions"])

                logger.debug(
                    f"Updating club user #{user.id} with data from {member_admin_url}"
                )
                user.account_id = account_id
                user.subscription_id = subscription_id
                user.customer_id = member["stripeCustomerId"]
                user.coupon = coupon_parts.get("coupon")
                user.update_expires_at(expires_at)
                user.has_feminine_name = has_feminine_name
                user.total_spend = math.ceil(member["totalSpendCents"] / 100)
                user.subscription_type = get_subscription_type(subscription)
                user.save()
        else:
            logger.info(f"Inactive: {member_admin_url}")

        logger.debug(f"Recording stats for {member_admin_url}")
        stats["quits"] += int(had_quit(member, stats_from, stats_to))
        stats["signups"] += int(had_signup(member, stats_from, stats_to))
        stats["trials"] += int(had_trial(member, stats_from, stats_to))

    logger.info("Processing remaining Discord users who are not in Memberful")
    remaining_users = (
        user for user in ClubUser.members_listing() if user.id not in seen_discord_ids
    )
    extra_users_ids = []
    for user in remaining_users:
        if user.id in (ClubMemberID.HONZA, ClubMemberID.HONZA_TEST):
            logger.debug(f"Skipping admin account #{user.id}")
        elif user.is_bot:
            logger.debug(f"Skipping bot account #{user.id}")
        else:
            logger.warning(
                f"Club user #{user.id} is on Discord, but doesn't have a Memberful account!"
            )
            logger.debug(f"User #{user.id}:\n{pformat(model_to_dict(user))}")
            extra_users_ids.append(user.id)
    if extra_users_ids:
        discord_task.run(report_extra_users, extra_users_ids)

    logger.info("Loading stats history from file to db")
    Members.drop_table()
    Members.create_table()
    history_path.touch(exist_ok=True)
    with history_path.open() as f:
        for line in f:
            Members.deserialize(line)

    month = f"{today:%Y-%m}"
    logger.info(f"Recording {month} stats")

    logger.debug("Recording stats")
    Members.record(month=month, name="members", count=ClubUser.members_count())
    Members.record(month=month, name="members_f", count=ClubUser.feminine_names_count())
    for subscription_type, count in ClubUser.subscription_types_breakdown().items():
        Members.record(
            month=month, name=f"subscription_types_{subscription_type}", count=count
        )
    for stat_name, count in stats.items():
        Members.record(month=month, name=f"subscriptions_{stat_name}", count=count)

    logger.info("Saving stats history to a file")
    with history_path.open("w") as f:
        for db_object in Members.history():
            f.write(db_object.serialize())


@db.connection_context()
async def report_extra_users(client: ClubClient, extra_users_ids: list[int]):
    logger.info("Prevent mistakes caused by out-of-sync data")
    extra_users = []
    for extra_user_id in extra_users_ids:
        try:
            extra_users.append(await client.club_guild.fetch_member(extra_user_id))
        except NotFound:
            logger.info(f"User #{extra_user_id} is not on Discord anymore, skipping")
    if extra_users:
        logger.info(f"Verified {len(extra_users)} users, reporting them")
        channel = await client.fetch_channel(ClubChannelID.BUSINESS)
        with mutating_discord(channel) as proxy:
            await proxy.send(
                "⚠️ Vypadá to, že tito členové nemají účet na Memberful: "
                f"{', '.join(user.mention for user in extra_users)}"
            )
    else:
        logger.info("After all, there are no users to report")


def get_active_subscription(
    subscriptions: list[SubscriptionEntity], today: date = None
) -> SubscriptionEntity:
    today = today or date.today()
    subscriptions = [
        subscription
        for subscription in subscriptions
        if (
            subscription["active"]
            and timestamp_to_date(subscription["activatedAt"]) <= today
            and (
                is_individual_plan(subscription["plan"])
                or is_group_plan(subscription["plan"])
            )
        )
    ]
    if len(subscriptions) > 1:
        overlapping_subscriptions = [
            subscription
            for subscription in subscriptions
            if timestamp_to_date(subscription["activatedAt"]) == today
        ]
        try:
            return overlapping_subscriptions[0]
        except IndexError:
            raise ValueError("Multiple active subscriptions")
    try:
        return subscriptions[0]
    except IndexError:
        raise ValueError("No active subscriptions")


def is_active(subscriptions: list[SubscriptionEntity]) -> bool:
    return any(subscription["active"] for subscription in subscriptions)


def get_expires_at(subscriptions: list[SubscriptionEntity]) -> datetime:
    return timestamp_to_datetime(
        max(
            subscription["expiresAt"]
            for subscription in subscriptions
            if subscription["active"]
        )
    )


def get_coupon(subscription: SubscriptionEntity) -> str | None:
    if subscription["coupon"]:
        return subscription["coupon"]["code"]

    orders = list(
        sorted(subscription["orders"], key=itemgetter("createdAt"), reverse=True)
    )
    try:
        last_order = orders[0]
        if not last_order["coupon"]:
            return None
        return last_order["coupon"]["code"]
    except IndexError:
        return None


def get_subscription_type(
    subscription: SubscriptionEntity, today: date | None = None
) -> SubscriptionType:
    plan = subscription["plan"]
    today = today or date.today()
    if is_sponsor_plan(plan):
        return SubscriptionType.SPONSOR
    if is_partner_plan(plan):
        return SubscriptionType.PARTNER
    if is_individual_plan(plan):
        if coupon := get_coupon(subscription):
            if coupon.startswith("FINAID"):
                return SubscriptionType.FINAID
            if coupon.startswith("THANKYOU"):
                return SubscriptionType.FREE
        if trial_end_at := subscription["trialEndAt"]:
            if timestamp_to_date(trial_end_at) >= today:
                return SubscriptionType.TRIAL
        if plan["intervalUnit"] == "month":
            return SubscriptionType.MONTHLY
        if plan["intervalUnit"] == "year":
            return SubscriptionType.YEARLY
    raise ValueError(f"Unknown subscription type: {subscription}")


def is_individual_subscription(subscription: SubscriptionEntity) -> bool:
    try:
        # In this context the 'today' parameter doesn't matter,
        # because it only influences how TRIAL subscription is evaluated.
        # If the subscription is not evaluated as TRIAL, then it's either
        # MONTHLY or YEARLY.
        return get_subscription_type(subscription) in [
            SubscriptionType.TRIAL,
            SubscriptionType.MONTHLY,
            SubscriptionType.YEARLY,
        ]
    except ValueError:
        return False


def had_signup(member: MemberEntity, from_date: date, to_date: date) -> bool:
    for subscription in member["subscriptions"]:
        if (
            not is_individual_subscription(subscription)
            or not subscription["trialEndAt"]
        ):
            continue
        orders_after_trial = [
            order
            for order in subscription["orders"]
            if order["createdAt"] > subscription["trialEndAt"]
        ]
        if orders_after_trial:
            signup_on = min(
                timestamp_to_date(order["createdAt"]) for order in orders_after_trial
            )
            return signup_on >= from_date and signup_on <= to_date
    return False


def had_trial(member: MemberEntity, from_date: date, to_date: date) -> bool:
    for subscription in member["subscriptions"]:
        if not is_individual_subscription(subscription):
            continue
        if trial_start_at := subscription["trialStartAt"]:
            trial_start_on = timestamp_to_date(trial_start_at)
            if trial_start_on > from_date and trial_start_on < to_date:
                return True
        if trial_end_at := subscription["trialEndAt"]:
            trial_end_on = timestamp_to_date(trial_end_at)
            if trial_end_on > from_date and trial_end_on < to_date:
                return True
    return False


def had_quit(member: MemberEntity, from_date: date, to_date: date) -> bool:
    if is_active(member["subscriptions"]):
        return False
    for subscription in member["subscriptions"]:
        if (
            not is_individual_subscription(subscription)
            or member["totalSpendCents"] == 0
        ):
            continue
        if subscription["expiresAt"]:
            expires_on = timestamp_to_date(subscription["expiresAt"])
            if expires_on >= from_date and expires_on < to_date:
                return True
    return False
