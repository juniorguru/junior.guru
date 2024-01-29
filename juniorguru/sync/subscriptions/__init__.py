import itertools
from datetime import date, datetime, time, timezone
from operator import itemgetter
from pathlib import Path
from pprint import pformat
from typing import Generator

import click

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.coupons import parse_coupon
from juniorguru.lib.memberful import MemberfulAPI
from juniorguru.models.base import db
from juniorguru.models.feminine_name import FeminineName
from juniorguru.models.partner import Partner
from juniorguru.models.subscription import (
    SubscriptionActivity,
    SubscriptionActivityType,
    SubscriptionType,
)


ACTIVITIES_GQL_PATH = Path(__file__).parent / "activities.gql"

ACTIVITY_TYPES_MAPPING = {
    "new_order": SubscriptionActivityType.ORDER,
    "renewal": SubscriptionActivityType.ORDER,
    "gift_activated": SubscriptionActivityType.ORDER,
    "subscription_deactivated": SubscriptionActivityType.DEACTIVATION,
    "subscription_deleted": SubscriptionActivityType.DEACTIVATION,
    "order_suspended": SubscriptionActivityType.DEACTIVATION,
}

SUBSCRIPTIONS_GQL_PATH = Path(__file__).parent / "subscriptions.gql"

SUBSCRIPTION_TYPES_MAPPING = {
    "thankyou": SubscriptionType.FREE,
    "thankyouforever": SubscriptionType.FREE,
    "thankyouteam": SubscriptionType.FREE,
    "patreon": SubscriptionType.FREE,
    "github": SubscriptionType.FREE,
    "founders": SubscriptionType.FREE,
    "coreskill": SubscriptionType.FREE,
    "studentcoreskill": SubscriptionType.FREE,
    "finaid": SubscriptionType.FINAID,
}


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["partners", "feminine-names"])
@click.option("--from-date", default="2021-01-01", type=date.fromisoformat)
@click.option("--multiple-products-date", default="2023-12-01", type=date.fromisoformat)
@click.option(
    "--history-path",
    default="juniorguru/data/subscription_activities.jsonl",
    type=click.Path(exists=True, path_type=Path),
)
@click.option("--clear-history/--keep-history", default=False)
@db.connection_context()
def main(from_date, multiple_products_date, history_path, clear_history):
    logger.info("Preparing")
    memberful = MemberfulAPI()

    SubscriptionActivity.drop_table()
    SubscriptionActivity.create_table()

    subscripton_types_mapping = {
        **{
            parse_coupon(coupon)["slug"]: SubscriptionType.PARTNER
            for coupon in Partner.coupons()
        },
        **{
            parse_coupon(coupon)["slug"]: SubscriptionType.STUDENT
            for coupon in Partner.student_coupons()
        },
        **SUBSCRIPTION_TYPES_MAPPING,
    }

    # The result of this function will be stored in history, because we cannot store
    # full names of members. If we change how we classify feminine names, there's no
    # way to go back and reclassify the names in the history (without clearing the history).
    def has_feminine_name(name) -> bool:
        return FeminineName.is_feminine(name.strip())

    logger.info("Reading history from a file")
    if clear_history:
        history_path.write_text("")
    else:
        with history_path.open() as f:
            for line in f:
                SubscriptionActivity.deserialize(line)
    from_date = SubscriptionActivity.history_end_on() or from_date

    logger.info(f"Fetching activities from Memberful API, since {from_date}")
    # This heavily relies on history. If there's no history, it will fetch everything
    # since the beginning of time. That's very slow and won't finish, because Memberful API
    # will ban the IP address until the next day. It can be done with cache and different
    # IP addresses (like starting over tethering using LTE of my phone, and re-starting over WiFi).
    queries = (
        memberful.get_nodes(
            ACTIVITIES_GQL_PATH.read_text(),
            dict(
                type=type,
                createdAt=dict(
                    gte=get_timestamp(from_date),
                    lt=get_timestamp(multiple_products_date),
                ),
            ),
        )
        for type in ACTIVITY_TYPES_MAPPING
    )
    for activity in logger.progress(itertools.chain.from_iterable(queries)):
        try:
            account_id = int(activity["member"]["id"])
        except (KeyError, TypeError):
            logger.debug(f"Activity with no account ID, skipping:\n{pformat(activity)}")
        else:
            happened_at = datetime.utcfromtimestamp(activity["createdAt"])
            SubscriptionActivity.add(
                account_id=account_id,
                account_has_feminine_name=has_feminine_name(
                    activity["member"]["fullName"]
                ),
                happened_on=happened_at.date(),
                happened_at=happened_at,
                type=ACTIVITY_TYPES_MAPPING[activity["type"]],
            )
    logger.info(f"Finished with {SubscriptionActivity.total_count()} activities")

    logger.info("Fetching subscriptions from Memberful API")
    # There is no filtering by date, so we need to fetch everything every time. One could
    # say that in such case there's no reason to save the data to history, but the reason
    # we do it is to have a backup (and a git commits to inspect) in case there is something
    # messing with the data again.
    subscriptions = memberful.get_nodes(SUBSCRIPTIONS_GQL_PATH.read_text())
    for subscription in logger.progress(subscriptions):
        if (
            subscription["createdAt"] >= get_timestamp(multiple_products_date)
            and not subscription["plan"]["planGroup"]
        ):
            logger.debug(f"Not a club subscription, skipping:\n{pformat(subscription)}")
            continue
        for activity in activities_from_subscription(subscription):
            activity["account_has_feminine_name"] = has_feminine_name(
                subscription["member"]["fullName"]
            )
            SubscriptionActivity.add(**activity)
    logger.info(f"Finished with {SubscriptionActivity.total_count()} activities")

    logger.info("Saving history to a file")
    with history_path.open("w") as f:
        for db_object in SubscriptionActivity.history():
            f.write(db_object.serialize())

    logger.info("Classifying subscription types")
    # History only stores coupon slug, so this is done as part of post-processing.
    # It's better than to store the subscription type in the history, because
    # this way over time we can change how the subscription types are classified.
    for activity in SubscriptionActivity.select():
        try:
            activity.subscription_type = subscripton_types_mapping[
                activity.order_coupon_slug
            ]
        except KeyError:
            activity.subscription_type = SubscriptionType.INDIVIDUAL
        activity.save()

    logger.info("Cleansing data")
    SubscriptionActivity.cleanse_data()


def activities_from_subscription(subscription: dict) -> Generator[dict, None, None]:
    account_id = int(subscription["member"]["id"])
    subscription_interval = subscription["plan"]["intervalUnit"]
    subscription_coupon_slug = get_coupon_slug(subscription["coupon"])

    created_at = datetime.utcfromtimestamp(subscription["createdAt"])
    yield dict(
        account_id=account_id,
        type=SubscriptionActivityType.ORDER,
        happened_on=created_at.date(),
        happened_at=created_at,
        subscription_interval=subscription_interval,
        order_coupon_slug=subscription_coupon_slug,
    )
    expires_at = datetime.utcfromtimestamp(subscription["expiresAt"])
    yield dict(
        account_id=account_id,
        type=SubscriptionActivityType.DEACTIVATION,
        happened_on=expires_at.date(),
        happened_at=expires_at,
        subscription_interval=subscription_interval,
        order_coupon_slug=subscription_coupon_slug,
    )

    if subscription["activatedAt"]:
        activated_at = datetime.utcfromtimestamp(subscription["activatedAt"])
        yield dict(
            account_id=account_id,
            type=SubscriptionActivityType.ORDER,
            happened_on=activated_at.date(),
            happened_at=activated_at,
            subscription_interval=subscription_interval,
            order_coupon_slug=subscription_coupon_slug,
        )
    if subscription["trialStartAt"]:
        trial_start_at = datetime.utcfromtimestamp(subscription["trialStartAt"])
        yield dict(
            account_id=account_id,
            type=SubscriptionActivityType.TRIAL_START,
            happened_on=trial_start_at.date(),
            happened_at=trial_start_at,
            subscription_interval=subscription_interval,
            order_coupon_slug=subscription_coupon_slug,
        )
    if subscription["trialEndAt"]:
        trial_end_at = datetime.utcfromtimestamp(subscription["trialEndAt"])
        yield dict(
            account_id=account_id,
            type=SubscriptionActivityType.TRIAL_END,
            happened_on=trial_end_at.date(),
            happened_at=trial_end_at,
            subscription_interval=subscription_interval,
            order_coupon_slug=subscription_coupon_slug,
        )

    orders = sorted(subscription["orders"], key=itemgetter("createdAt"), reverse=True)
    for i, order in enumerate(orders):
        if subscription_coupon_slug and i == 0:
            order_coupon_slug = subscription_coupon_slug
        else:
            order_coupon_slug = get_coupon_slug(order["coupon"])

        order_created_at = datetime.utcfromtimestamp(order["createdAt"])
        yield dict(
            account_id=account_id,
            type=SubscriptionActivityType.ORDER,
            happened_on=order_created_at.date(),
            happened_at=order_created_at,
            subscription_interval=subscription["plan"]["intervalUnit"],
            order_coupon_slug=order_coupon_slug,
        )


def get_timestamp(date: date) -> int:
    return int(datetime.combine(date, time(), tzinfo=timezone.utc).timestamp())


def get_coupon_slug(coupon_data: dict) -> None | str:
    if coupon := (coupon_data or {}).get("code"):
        return parse_coupon(coupon)["slug"]
    return None
