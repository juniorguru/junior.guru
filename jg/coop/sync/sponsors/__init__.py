from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, Literal, TypedDict

import click
import yaml
from pydantic import BaseModel, HttpUrl

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.coupons import parse_coupon
from jg.coop.lib.images import PostersCache, render_image_file
from jg.coop.lib.memberful import MemberfulAPI
from jg.coop.models.base import db
from jg.coop.models.sponsor import PastSponsor, Sponsor, SponsorTier


YAML_PATH = Path("jg/coop/data/sponsors.yml")

COUPONS_GQL_PATH = Path(__file__).parent / "coupons.gql"

IMAGES_DIR = Path("jg/coop/images")

LOGOS_DIR = IMAGES_DIR / "logos"

POSTERS_DIR = IMAGES_DIR / "posters-sponsors"

POSTER_SIZE = 700


logger = loggers.from_path(__file__)


class CouponEntity(TypedDict):
    code: str
    state: Literal["enabled", "disabled"]


class TierConfig(BaseModel):
    slug: str
    priority: int


class SponsorConfig(BaseModel):
    name: str
    slug: str
    url: HttpUrl
    tier: str | None = None
    periods: list[tuple[str, str | None]]
    note: str | None = None


class SponsorsConfig(BaseModel):
    tiers: list[TierConfig]
    registry: list[SponsorConfig]


@cli.sync_command()
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--clear-posters/--keep-posters", default=False)
@db.connection_context()
def main(today: date, clear_posters: bool):
    logger.debug("Initializing posters cache")
    posters = PostersCache(POSTERS_DIR)
    posters.init(clear=clear_posters)

    logger.debug("Resetting sponsors tables")
    db.drop_tables([Sponsor, SponsorTier, PastSponsor])
    db.create_tables([Sponsor, SponsorTier, PastSponsor])

    logger.info("Getting coupons data from Memberful")
    memberful = MemberfulAPI()
    coupons: Iterable[CouponEntity] = memberful.get_nodes(COUPONS_GQL_PATH.read_text())
    coupons_mapping = get_coupons_mapping(coupons)

    logger.info(f"Loading sponsors data from {YAML_PATH}")
    yaml_data = yaml.safe_load(YAML_PATH.read_text())
    sponsors = SponsorsConfig(**yaml_data)

    tiers = {
        tier.slug: SponsorTier.create(slug=tier.slug, priority=tier.priority)
        for tier in sponsors.tiers
    }
    logger.info(f"Tiers: {', '.join(tiers.keys())}")

    for sponsor in sponsors.registry:
        if renews_on := get_renews_on(sponsor.periods, today):
            logger.info(f"Sponsor {sponsor.name} ({sponsor.slug})")
            tier = tiers[sponsor.tier] if sponsor.tier else None

            logger.debug(f"Checking logo for {sponsor.slug!r} exists")
            logo_path = LOGOS_DIR / f"{sponsor.slug}.svg"
            if not logo_path.exists():
                logo_path = logo_path.with_suffix(".png")
            if not logo_path.exists():
                raise FileNotFoundError(
                    f"'There is no {sponsor.slug}.svg or .png inside {LOGOS_DIR}"
                )
            logo_path = logo_path.relative_to(IMAGES_DIR)

            logger.debug(f"Rendering poster for {sponsor.slug!r}")
            image_path = render_image_file(
                POSTER_SIZE,
                POSTER_SIZE,
                "sponsor.jinja",
                dict(sponsor_name=sponsor.name, sponsor_logo_path=logo_path, tier=tier),
                POSTERS_DIR,
                prefix=sponsor.slug,
            )
            poster_path = image_path.relative_to(IMAGES_DIR)
            posters.record(IMAGES_DIR / poster_path)

            logger.debug(f"Saving {sponsor.slug!r}")
            Sponsor.create(
                slug=sponsor.slug,
                name=sponsor.name,
                url=sponsor.url,
                tier=tier,
                renews_on=renews_on,
                coupon=coupons_mapping.get(sponsor.slug),
                logo_path=logo_path,
                poster_path=poster_path,
            )
        else:
            logger.info(f"Past sponsor {sponsor.name} ({sponsor.slug})")
            PastSponsor.create(
                slug=sponsor.slug,
                name=sponsor.name,
                url=sponsor.url,
            )

    posters.cleanup()
    logger.info(
        f"Created {Sponsor.count()} sponsors and {PastSponsor.count()} past sponsors"
    )


def get_coupons_mapping(coupons: Iterable[CouponEntity]) -> dict[str, str]:
    return {
        parse_coupon(coupon["code"])["slug"].lower(): coupon["code"]
        for coupon in coupons
        if coupon["state"] == "enabled"
    }


def get_renews_on(periods: list[tuple[str, str | None]], today: date) -> bool:
    current_period = sorted(periods, reverse=True)[0]
    period_start, period_end = current_period

    if period_end:
        year, month = map(int, period_end.split("-"))
        renew_date = next_month(date(year, month, 1))
        return None if renew_date < today else renew_date

    month = int(period_start.split("-")[1])
    pivot_date = date(today.year, month, 1)
    if pivot_date <= today.replace(day=1):
        return next_month(date(today.year + 1, month, 1))

    return next_month(pivot_date)


def next_month(month: date) -> date:
    return (month.replace(day=1) + timedelta(days=32)).replace(day=1)
