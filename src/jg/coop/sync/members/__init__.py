import math
from collections import defaultdict
from collections.abc import Iterable
from datetime import UTC, date, datetime, time
from enum import StrEnum
from operator import itemgetter
from pathlib import Path
from pprint import pformat
from typing import Literal, TypedDict

import click
from discord import NotFound
from playhouse.shortcuts import model_to_dict

from jg.coop.cli.sync import main as cli
from jg.coop.lib import charts, discord_task, loggers
from jg.coop.lib.discord_club import ClubChannelID, ClubClient, ClubMemberID
from jg.coop.lib.memberful import (
    MemberfulAPI,
    is_individual_plan,
    is_partner_plan,
    is_sponsor_plan,
    is_student_pass_coupon,
    memberful_url,
    timestamp_to_date,
    timestamp_to_datetime,
)
from jg.coop.lib.mutations import mutating_discord
from jg.coop.models.base import db
from jg.coop.models.club import ClubUser, SubscriptionType
from jg.coop.models.feminine_name import FeminineName
from jg.coop.models.members import MRR_BEGIN_ON, Members


logger = loggers.from_path(__file__)


MEMBERS_GQL_PATH = Path(__file__).parent / "members.gql"

ORDERS_GQL_PATH = Path(__file__).parent / "orders.gql"

MRR_YEARLY_MONTHS = 12

ADMIN_MEMBER_IDS = [ClubMemberID.HONZA, ClubMemberID.HONZA_TEST]


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


class OrderEntity(TypedDict):
    createdAt: int
    status: Literal["completed", "refunded", "suspended"]
    totalCents: int
    purchasable: dict | None


class AccountEntity(TypedDict):
    id: str
    discordUserId: str
    email: str
    fullName: str
    totalSpendCents: int
    stripeCustomerId: str
    subscriptions: list[SubscriptionEntity]


StatName = Literal["quits", "signups", "trials"]


@cli.sync_command(dependencies=["club-content", "feminine-names"])
@click.option(
    "--history-path",
    default="src/jg/coop/data/members.jsonl",
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

    accounts: Iterable[AccountEntity] = memberful.get_nodes(
        MEMBERS_GQL_PATH.read_text()
    )
    seen_discord_ids = set()

    stats_from = today.replace(day=1)
    stats_to = today
    stats: defaultdict[StatName, int] = defaultdict(int)

    for account in logger.progress(accounts):
        account_id = int(account["id"])
        account_admin_url = memberful_url(account_id)

        logger.info(f"Processing account {account_admin_url}")
        if is_active(account["subscriptions"]):
            try:
                discord_id = int(account["discordUserId"])  # raies TypeError if None
                member = ClubUser.get_by_id(discord_id)  # raises ClubUser.DoesNotExist
            except (TypeError, ClubUser.DoesNotExist):
                logger.warning(f"Member {account_admin_url} isn't on Discord")
            else:
                logger.debug(f"Identified as member #{member.id}")
                seen_discord_ids.add(member.id)

                subscription = get_active_subscription(account["subscriptions"])
                logger.debug(f"Subscription of {account_admin_url}: {subscription}")
                logger.debug(
                    f"Updating member #{member.id} with data from {account_admin_url}"
                )
                member.account_id = account_id
                member.customer_id = account["stripeCustomerId"]
                member.update_expires_at(get_expires_at(account["subscriptions"]))
                member.has_feminine_name = FeminineName.is_feminine(account["fullName"])
                member.total_spend = math.ceil(account["totalSpendCents"] / 100)
                member.subscription_type = get_subscription_type(subscription, today)
                member.save()
        else:
            logger.info(f"Inactive: {account_admin_url}")

        logger.debug(f"Recording stats for {account_admin_url}")
        stats["quits"] += int(had_quit(account, stats_from, stats_to))
        stats["signups"] += int(had_signup(account, stats_from, stats_to))
        stats["trials"] += int(had_trial(account, stats_from, stats_to))

    logger.info("Processing remaining Discord members who are not in Memberful")
    remaining_members = (
        member
        for member in ClubUser.members_listing()
        if member.id not in seen_discord_ids
    )
    trespassing_members_ids = []
    for member in remaining_members:
        if member.id in ADMIN_MEMBER_IDS:
            logger.debug(f"Adding subscription type to admin user #{member.id}")
            member.subscription_type = SubscriptionType.FREE
            member.save()
        elif member.is_bot:
            logger.debug(f"Skipping bot user #{member.id}")
        else:
            logger.warning(
                f"Discord member #{member.id} doesn't have a Memberful account!"
            )
            logger.debug(f"User #{member.id}:\n{pformat(model_to_dict(member))}")
            member.is_trespassing = True
            member.save()
            trespassing_members_ids.append(member.id)
    if trespassing_members_ids:
        discord_task.run(report_trespassing_members, trespassing_members_ids)

    logger.info("Checking consistency")
    for member in ClubUser.members_listing():
        if not member.subscription_type:
            raise ValueError(
                f"Member {memberful_url(member.account_id)} doesn't have a subscription type"
            )
    members_count = ClubUser.members_count()
    members_subscription_types_count = sum(
        ClubUser.subscription_types_breakdown().values()
    )
    if members_count != members_subscription_types_count:
        raise ValueError(
            f"Number of all members ({members_count}) isn't equal to a sum of members with a subscription type ({members_subscription_types_count})"
        )

    logger.info("Loading stats history from file to db")
    Members.drop_table()
    Members.create_table()
    history_path.touch(exist_ok=True)
    with history_path.open() as f:
        for line in f:
            Members.deserialize(line)

    logger.info("Getting orders from Memberful")
    orders_from = get_mrr_orders_from(MRR_BEGIN_ON)
    orders: list[OrderEntity] = list(
        memberful.get_nodes(
            ORDERS_GQL_PATH.read_text(),
            {"createdFrom": date_to_timestamp(orders_from)},
        )
    )
    logger.info(f"Got {len(orders)} orders created since {orders_from}")

    logger.info("Recording individual MRR")
    for mrr_month, mrr in get_mrr_history(orders, MRR_BEGIN_ON, today).items():
        Members.record(month=mrr_month, name="mrr_individuals", count=mrr)

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
async def report_trespassing_members(client: ClubClient, members_ids: list[int]):
    logger.info("Prevent mistakes caused by out-of-sync data")
    trespassing_members = []
    for member_id in members_ids:
        try:
            trespassing_members.append(await client.club_guild.fetch_member(member_id))
        except NotFound:
            logger.info(f"User #{member_id} is not on Discord anymore, skipping")
    if trespassing_members:
        logger.info(f"Verified {len(trespassing_members)} members, reporting them")
        channel = await client.fetch_channel(ClubChannelID.BUSINESS)
        with mutating_discord(channel) as proxy:
            await proxy.send(
                "⚠️ Vypadá to, že tito členové nemají účet na Memberful: "
                f"{', '.join(member.mention for member in trespassing_members)}"
            )
    else:
        logger.info("After all, there are no users to report")


def get_mrr_history(
    orders: Iterable[OrderEntity], begin_on: date, today: date
) -> dict[str, int]:
    """Calculates individual MRR for each month from begin_on to today"""
    orders = list(orders)
    return {
        f"{month:%Y-%m}": get_mrr(orders, month)
        for month in charts.months(begin_on, today)
    }


def get_mrr(orders: Iterable[OrderEntity], month: date) -> int:
    """Calculates individual MRR in CZK for the month of given date

    Sums paid orders on monthly individual plans created in the month,
    plus 1/12 of paid orders on yearly individual plans created in the
    last 12 months. Free orders, such as trials or 100% coupons, add nothing.
    """
    month_starts_on = month.replace(day=1)
    month_ends_on = charts.next_month(month_starts_on)
    yearly_starts_on = get_mrr_orders_from(month_starts_on)
    total_cents = 0.0
    for order in orders:
        if not is_individual_paid_order(order):
            continue
        created_on = timestamp_to_date(order["createdAt"])
        interval_unit = order["purchasable"]["intervalUnit"]
        if interval_unit == "month" and month_starts_on <= created_on < month_ends_on:
            total_cents += order["totalCents"]
        elif interval_unit == "year" and yearly_starts_on <= created_on < month_ends_on:
            total_cents += order["totalCents"] / MRR_YEARLY_MONTHS
    return round(total_cents / 100)


def is_individual_paid_order(order: OrderEntity) -> bool:
    plan = order["purchasable"]
    return (
        order["status"] == "completed"
        and order["totalCents"] > 0
        and plan is not None
        and "name" in plan
        and is_individual_plan(plan)
    )


def get_mrr_orders_from(month: date) -> date:
    """Returns the first day of the oldest month a yearly order still counts in MRR"""
    index = month.year * 12 + month.month - 1 - (MRR_YEARLY_MONTHS - 1)
    return date(index // 12, index % 12 + 1, 1)


def date_to_timestamp(day: date) -> int:
    return int(datetime.combine(day, time(), UTC).timestamp())


def get_active_subscription(
    subscriptions: list[SubscriptionEntity], today: date | None = None
) -> SubscriptionEntity:
    today = today or date.today()

    active_subscriptions = (
        subscription
        for subscription in subscriptions
        if subscription["active"]
        and timestamp_to_date(subscription["activatedAt"]) <= today
    )
    active_subscriptions_and_types = (
        (subscription, get_subscription_type_or_none(subscription, today=today))
        for subscription in active_subscriptions
    )
    active_club_subscriptions_and_types = [
        (subscription, subscription_type)
        for subscription, subscription_type in active_subscriptions_and_types
        if subscription_type is not None
    ]

    if len(active_club_subscriptions_and_types) == 1:
        return active_club_subscriptions_and_types[0][0]
    if len(active_club_subscriptions_and_types) < 1:
        raise ValueError("No active subscriptions")

    if len(active_club_subscriptions_and_types) == 2:
        # Tolerate having two active subscriptions where one is group
        # and the other is free (e.g. finaid and sponsored)
        pseudo_types_mapping = {
            SubscriptionType.TRIAL: "free",
            SubscriptionType.MONTHLY: "individual",
            SubscriptionType.YEARLY: "individual",
            SubscriptionType.SPONSOR: "group",
            SubscriptionType.PARTNER: "group",
            SubscriptionType.FINAID: "free",
            SubscriptionType.STUDENT_PASS: "free",
            SubscriptionType.FREE: "free",
        }
        assert set(pseudo_types_mapping.keys()) == set(SubscriptionType)

        subscription1, type1 = active_club_subscriptions_and_types[0]
        pseudo_type1 = pseudo_types_mapping[type1]
        subscription2, type2 = active_club_subscriptions_and_types[1]
        pseudo_type2 = pseudo_types_mapping[type2]

        if {pseudo_type1, pseudo_type2} == {"group", "free"}:
            return subscription1 if pseudo_type1 == "group" else subscription2

        # Tolerate having two active subscriptions where the start of the
        # subsequent subscription overlaps with the current one for one day
        if timestamp_to_date(subscription1["activatedAt"]) == today:
            return subscription1
        if timestamp_to_date(subscription2["activatedAt"]) == today:
            return subscription2

    raise ValueError("Multiple active subscriptions")


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

    orders = sorted(subscription["orders"], key=itemgetter("createdAt"), reverse=True)
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
            if is_student_pass_coupon(coupon) and not is_paid_after_coupon(
                subscription
            ):
                return SubscriptionType.STUDENT_PASS
            if coupon.startswith("FINAID"):
                return SubscriptionType.FINAID
            if coupon.startswith("THANKYOU"):
                return SubscriptionType.FREE
        if (trial_end_at := subscription["trialEndAt"]) and timestamp_to_date(
            trial_end_at
        ) >= today:
            return SubscriptionType.TRIAL
        if plan["intervalUnit"] == "month":
            return SubscriptionType.MONTHLY
        if plan["intervalUnit"] == "year":
            return SubscriptionType.YEARLY
    raise ValueError(f"Unknown subscription type: {subscription}")


def is_paid_after_coupon(subscription: SubscriptionEntity) -> bool:
    """
    Checks whether the member paid for an order which came after a one-time coupon

    A one-time coupon, such as the student pass, applies to the first order
    after the trial. The subscription can keep the coupon even after that,
    but once a later order has no coupon, it's a regular subscription.
    """
    orders = sorted(subscription["orders"], key=itemgetter("createdAt"))
    return len(orders) > 1 and not orders[-1]["coupon"]


def get_subscription_type_or_none(
    subscription: SubscriptionEntity, today: date | None = None
) -> SubscriptionType | None:
    try:
        return get_subscription_type(subscription, today)
    except ValueError:
        return None


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


def had_signup(account: AccountEntity, from_date: date, to_date: date) -> bool:
    for subscription in account["subscriptions"]:
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


def had_trial(account: AccountEntity, from_date: date, to_date: date) -> bool:
    for subscription in account["subscriptions"]:
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


def had_quit(account: AccountEntity, from_date: date, to_date: date) -> bool:
    if is_active(account["subscriptions"]):
        return False
    for subscription in account["subscriptions"]:
        if (
            not is_individual_subscription(subscription)
            or account["totalSpendCents"] == 0
        ):
            continue
        if subscription["expiresAt"]:
            expires_on = timestamp_to_date(subscription["expiresAt"])
            if expires_on >= from_date and expires_on < to_date:
                return True
    return False
