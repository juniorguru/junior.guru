from datetime import datetime

import arrow

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers, mutations
from jg.coop.lib.memberful import MemberfulAPI
from jg.coop.models.base import db
from jg.coop.models.sponsor import Sponsor


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["subscriptions", "organizations"])
@db.connection_context()
def main():
    return  # TODO SPONSORS, temporarily disabled until rewritten
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
        for member in sponsor.list_members:
            logger_s.debug(f"Processing {member.display_name}")
            if member.expires_at.date() < sponsor.renews_on:
                logger_s.warning(
                    f"{member!r} {member.expires_at.date()} < {sponsor.renews_on}"
                )
                params = dict(
                    id=member.subscription_id,
                    expiresAt=int(arrow.get(sponsor.renews_on).timestamp()),
                )
                if align_subscription(memberful, mutation, params):
                    member.expires_at = datetime.combine(
                        sponsor.renews_on, datetime.min.time()
                    )
                    member.save()
                    logger_s.info(
                        f"{member!r} subscription updated to expire on {member.expires_at.date()}"
                    )
            else:
                logger_s.debug(
                    f"{member!r} {member.expires_at.date()} ≥ {sponsor.renews_on}"
                )


@mutations.mutates_memberful()
def align_subscription(memberful, mutation, params):
    return memberful.mutate(mutation, params)
