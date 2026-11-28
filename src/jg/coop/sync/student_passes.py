from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers, mutations
from jg.coop.lib.memberful import (
    STUDENT_PASS_DISCOUNT_ID,
    MemberfulAPI,
    parse_created_coupons,
)
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseProvider


CREATE_COUPONS_MUTATION = """
    mutation ($discountId: ID!, $coupons: [CouponInput!]!) {
        createCoupons(discountId: $discountId, coupons: $coupons) {
            coupons {
                code
            }
            errors {
                key
                messages {
                    attribute
                    message
                }
            }
        }
    }
"""


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["course-providers"])
@db.connection_context()
def main():
    codes = [
        course_provider.student_pass_coupon
        for course_provider in CourseProvider.student_pass_listing()
    ]
    logger.info(f"Course providers with student passes: {len(codes)}")
    if not codes:
        return
    logger.info(f"Ensuring coupon codes exist: {', '.join(codes)}")
    variables = {
        "discountId": str(STUDENT_PASS_DISCOUNT_ID),
        "coupons": [{"code": code} for code in codes],
    }
    if payload := create_coupons(MemberfulAPI(), variables):
        created_codes = parse_created_coupons(payload)
        logger.info(f"Created coupon codes: {', '.join(created_codes) or '-'}")


@mutations.mutates_memberful()
def create_coupons(memberful: MemberfulAPI, variables: dict) -> dict:
    return memberful.mutate(CREATE_COUPONS_MUTATION, variables)
