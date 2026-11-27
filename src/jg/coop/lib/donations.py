"""Donations to junior.guru: Czech QR payments and how much donors cover"""

import io
import math

from qrplatba import QRPlatbaGenerator


DONATION_AMOUNT_CZK = 499

DONATION_MESSAGE = "LOVE pro junior.guru"


def coverage_ptc(
    revenue_breakdown: dict[str, int], cost: int, category: str
) -> int | None:
    """Percentage of costs covered by given revenue category, rounded down to stay honest"""
    if cost <= 0:
        return None
    return math.floor(revenue_breakdown.get(category, 0) * 100 / cost)


def qr_payment_svg(
    account: str, bic: str, amount: int, variable_symbol: str, message: str
) -> str:
    """Czech QR payment code as an SVG element suitable for inlining into HTML"""
    stream = io.BytesIO()
    get_generator(account, bic, amount, variable_symbol, message).make_image().save(
        stream
    )
    svg = stream.getvalue().decode()
    return svg[svg.index("<svg") :]


def qr_payment_spayd(
    account: str, bic: str, amount: int, variable_symbol: str, message: str
) -> str:
    return get_generator(account, bic, amount, variable_symbol, message).get_text()


def get_generator(
    account: str, bic: str, amount: int, variable_symbol: str, message: str
) -> QRPlatbaGenerator:
    return QRPlatbaGenerator(
        account,
        bic=bic,
        amount=amount,
        currency="CZK",
        x_vs=variable_symbol,
        message=message,
    )
