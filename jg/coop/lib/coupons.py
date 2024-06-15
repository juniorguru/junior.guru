import re
from typing import TypedDict


COUPON_RE = re.compile(
    r"""
        ^
            (?P<slug>
                [A-Z0-9]+
                [A-Z]+
            )
            (?P<suffix>[0-9]{5,})
        $
    """,
    re.VERBOSE,
)


class CouponParts(TypedDict):
    slug: str
    coupon: str


def parse_coupon(coupon: str) -> CouponParts:
    if match := COUPON_RE.match(coupon):
        parts = match.groupdict()
        parts["coupon"] = "".join(
            [
                parts["slug"],
                parts["suffix"],
            ]
        )
        parts["slug"] = parts["slug"].lower()
        return {key: value for key, value in parts.items() if value is not None}
    return {"slug": coupon.lower(), "coupon": coupon}
