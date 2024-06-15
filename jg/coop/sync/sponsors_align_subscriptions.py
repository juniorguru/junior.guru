from datetime import datetime

import arrow

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers, mutations
from jg.coop.lib.memberful import MemberfulAPI
from jg.coop.models.base import db
from jg.coop.models.sponsor import Sponsor


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["subscriptions", "sponsors"])
@db.connection_context()
def main():
    memberful = MemberfulAPI()
    mutation = """
        mutation ($id: ID!, $expiresAt: Int!) {
            subscriptionChangeExpirationTime(id: $id, expiresAt: $expiresAt) {
                subscription {
                    id
                    expiresAt
                }
            }
        }
    """

    for sponsor in Sponsor.listing():
        logger_s = logger[sponsor.slug]
        logger_s.info(f"Sponsor renews on {sponsor.renews_on}")
        for employee in sponsor.list_members:
            logger_s.debug(f"Processing {employee.display_name}")
            if employee.expires_at.date() < sponsor.renews_on:
                logger_s.warning(
                    f"{employee!r} {employee.expires_at.date()} < {sponsor.renews_on}"
                )
                params = dict(
                    id=employee.subscription_id,
                    expiresAt=int(arrow.get(sponsor.renews_on).timestamp()),
                )
                if align_subscription(memberful, mutation, params):
                    employee.expires_at = datetime.combine(
                        sponsor.renews_on, datetime.min.time()
                    )
                    employee.save()
                    logger_s.info(
                        f"{employee!r} subscription updated to expire on {employee.expires_at.date()}"
                    )
            else:
                logger_s.debug(
                    f"{employee!r} {employee.expires_at.date()} ≥ {sponsor.renews_on}"
                )


@mutations.mutates_memberful()
def align_subscription(memberful, mutation, params):
    return memberful.mutate(mutation, params)
