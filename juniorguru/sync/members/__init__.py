import math
from datetime import date, datetime
from operator import itemgetter
from pathlib import Path
from pprint import pformat

from discord import NotFound
from playhouse.shortcuts import model_to_dict

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.coupons import parse_coupon
from juniorguru.lib.discord_club import ClubChannelID, ClubClient, ClubMemberID
from juniorguru.lib.memberful import MemberfulAPI, memberful_url
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubUser
from juniorguru.models.feminine_name import FeminineName
from juniorguru.models.subscription import SubscriptionActivity


logger = loggers.from_path(__file__)


MEMBERS_GQL_PATH = Path(__file__).parent / "members.gql"


@cli.sync_command(
    dependencies=["club-content", "partners", "feminine-names", "subscriptions"]
)
@db.connection_context()
def main():
    logger.info("Getting data from Memberful")
    memberful = MemberfulAPI()

    members = memberful.get_nodes(MEMBERS_GQL_PATH.read_text())
    seen_discord_ids = set()
    for member in logger.progress(members):
        account_id = int(member["id"])
        member_admin_url = memberful_url(account_id)
        logger.debug(f"Processing member {member_admin_url}")
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

            subscribed_at = SubscriptionActivity.account_subscribed_at(account_id)
            if not subscribed_at:
                raise ValueError(
                    f"Member {member_admin_url} has no subscription activities"
                )
            subscribed_days = SubscriptionActivity.account_subscribed_days(account_id)

            subscription = get_active_subscription(member["subscriptions"])
            coupon = get_coupon(subscription)
            coupon_parts = parse_coupon(coupon) if coupon else {}
            expires_at = get_expires_at(member["subscriptions"])

            logger.debug(
                f"Updating club user #{user.id} with data from {member_admin_url}"
            )
            user.account_id = account_id
            user.subscription_id = str(subscription["id"])
            user.customer_id = member["stripeCustomerId"]
            user.subscribed_at = subscribed_at
            user.subscribed_days = subscribed_days
            user.coupon = coupon_parts.get("coupon")
            user.update_expires_at(expires_at)
            user.has_feminine_name = has_feminine_name
            user.total_spend = math.ceil(member["totalSpendCents"] / 100)
            user.save()

    logger.info(
        "Processing remaining club users who are on Discord, but not in Memberful"
    )
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
        discord_sync.run(report_extra_users, extra_users_ids)


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
        channel = await client.fetch_channel(ClubChannelID.MODERATION)
        with mutating_discord(channel) as proxy:
            await proxy.send(
                "⚠️ Vypadá to, že tito členové nemají účet na Memberful: "
                f"{', '.join(user.mention for user in extra_users)}"
            )
    else:
        logger.info("After all, there are no users to report")


def get_active_subscription(subscriptions: list[dict], today: date = None) -> dict:
    today = today or date.today()
    subscriptions = [
        s
        for s in subscriptions
        if s["active"] and datetime.utcfromtimestamp(s["activatedAt"]).date() <= today and s["plan"]["planGroup"]
    ]
    if len(subscriptions) > 1:
        try:
            return [
                s
                for s in subscriptions
                if datetime.utcfromtimestamp(s["activatedAt"]).date() == today
            ][0]
        except IndexError:
            raise ValueError("Multiple active subscriptions")
    try:
        return subscriptions[0]
    except IndexError:
        raise ValueError("No active subscriptions")


def get_expires_at(subscriptions: list[dict]) -> datetime:
    return datetime.utcfromtimestamp(
        max(
            subscription["expiresAt"]
            for subscription in subscriptions
            if subscription["active"]
        )
    )


def get_coupon(subscription):
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
