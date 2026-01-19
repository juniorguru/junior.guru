import re
from datetime import date, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Annotated, Any, Iterable, Literal, TypedDict

import click
import yaml
from pydantic import (
    AfterValidator,
    HttpUrl,
    ValidationInfo,
)

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.images import PostersCache, render_image_file
from jg.coop.lib.memberful import (
    MemberfulAPI,
    from_cents,
    is_public_plan,
    is_sponsor_plan,
    parse_tier_name,
)
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.partner import Partner
from jg.coop.models.sponsor import PastSponsor, Sponsor, SponsorTier


SPONSORS_YAML_PATH = Path("src/jg/coop/data/sponsors.yml")

PARTNERS_YAML_PATH = Path("src/jg/coop/data/partners.yml")

PLANS_GQL_PATH = Path(__file__).parent / "plans.gql"

SUBSCRIPTION_GQL_PATH = Path(__file__).parent / "subscription.gql"

IMAGES_DIR = Path("src/jg/coop/images")

LOGOS_DIR = IMAGES_DIR / "logos"

LOGOS_CSS_PATH = Path("src/jg/coop/css/content/_logos.scss")

LOGOS_CSS_RE = re.compile(r"\.logos-tier-(\d+)\b")

POSTERS_DIR = IMAGES_DIR / "posters-sponsors"

POSTER_SIZE = 700

TIERS_EXTRAS = {
    "Budujeme brand": dict(max_sponsors=4, courses_highlight=True),
    "Poskytujeme kurzy": dict(courses_highlight=True),
}


logger = loggers.from_path(__file__)


class CouponEntity(TypedDict):
    code: str
    state: Literal["enabled", "disabled"]


class PlanEntity(TypedDict):
    id: str
    name: str
    forSale: bool
    priceCents: int
    additionalMemberPriceCents: int | None


class NodeID(TypedDict):
    id: str


class Edge(TypedDict):
    node: NodeID


class PageInfo(TypedDict):
    hasNextPage: bool


class MembersCollection(TypedDict):
    edges: list[Edge]
    pageInfo: PageInfo


class SubscriptionEntity(TypedDict):
    plan: NodeID
    members: MembersCollection


def check_subscription(value: HttpUrl | None, info: ValidationInfo) -> HttpUrl:
    if value:
        parse_subscription_id(value)  # raises ValueError
    return value


def check_plan(value: HttpUrl | None, info: ValidationInfo) -> HttpUrl:
    if value:
        parse_plan_id(value)  # raises ValueError
    if value and info.data["subscription"]:
        raise ValueError(
            "Sponsor cannot have both plan and subscription specified: "
            f"{value!r} vs {info.data['subscription']!r}"
        )
    if not value and not info.data["subscription"]:
        raise ValueError(
            "Sponsor must have either plan or subscription specified: "
            f"{value!r} vs {info.data['subscription']!r}"
        )
    return value


class OrganizationConfig(YAMLConfig):
    name: str
    slug: str
    url: HttpUrl | None = None
    cz_business_id: int | None = None
    sk_business_id: int | None = None
    subscription: Annotated[HttpUrl | None, AfterValidator(check_subscription)] = None
    plan: Annotated[HttpUrl | None, AfterValidator(check_plan)] = None


class SponsorConfig(OrganizationConfig):
    periods: list[tuple[str, str | None]]
    note: str | None = None


class SponsorsConfig(YAMLConfig):
    registry: list[SponsorConfig]


class PartnerConfig(OrganizationConfig):
    start_on: str
    is_free: bool = True
    note: str


class PartnersConfig(YAMLConfig):
    default_plan: HttpUrl
    registry: list[PartnerConfig]


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

    logger.info("Getting data from Memberful")
    memberful = MemberfulAPI()
    plans: Iterable[PlanEntity] = memberful.get(PLANS_GQL_PATH.read_text())["plans"]

    logger.info("Creating sponsors tiers")
    tiers_by_plan_id: dict[int, SponsorTier] = {
        tier_data["plan_id"]: SponsorTier.create(**tier_data)
        for tier_data in prepare_tiers(plans, extras=TIERS_EXTRAS)
    }
    check_css_integrity(tiers_by_plan_id.values(), LOGOS_CSS_PATH.read_text())

    logger.info(f"Loading sponsors data from {SPONSORS_YAML_PATH}")
    sponsors_yaml_data = yaml.safe_load(SPONSORS_YAML_PATH.read_text())
    sponsors = SponsorsConfig(**sponsors_yaml_data)

    for sponsor in sponsors.registry:
        start_on = get_start_on(sponsor.periods)
        renews_on = get_renews_on(sponsor.periods, today)
        if start_on > today:
            logger.warning(f"Future sponsor {sponsor.name} ({sponsor.slug})")
        elif renews_on and renews_on > today:
            logger.info(
                f"Active sponsor {sponsor.name} ({sponsor.slug}), renews on {renews_on}"
            )

            logger.debug("Checking plan, subscription, and figuring out tier")
            subscription_id = None
            if sponsor.plan:
                plan_id = parse_plan_id(sponsor.plan)
                tier = tiers_by_plan_id[plan_id]
                account_ids = []
            elif sponsor.subscription:
                subscription_id = parse_subscription_id(sponsor.subscription)
                subscription = memberful.get(
                    SUBSCRIPTION_GQL_PATH.read_text(), dict(id=subscription_id)
                )["subscription"]
                plan_id = get_plan_id(subscription)
                tier = tiers_by_plan_id[plan_id]
                account_ids = get_account_ids(subscription)
            else:
                raise ValueError("Sponsor must have either plan or subscription")
            logger.debug(f"Using tier {tier.name!r} for {sponsor.slug!r}")

            logger.debug("Processing note")
            note = parse_note(sponsor.note)

            logger.debug(f"Checking logo for {sponsor.slug!r} exists")
            logo_path = find_logo(sponsor.slug)

            logger.debug(f"Rendering poster for {sponsor.slug!r}")
            image_path = render_image_file(
                POSTER_SIZE,
                POSTER_SIZE,
                "sponsor.jinja",
                dict(
                    sponsor_name=sponsor.name,
                    sponsor_logo_path=logo_path,
                    tier_priority=tier.priority,
                ),
                POSTERS_DIR,
                prefix=sponsor.slug,
            )
            poster_path = image_path.relative_to(IMAGES_DIR)
            posters.record(IMAGES_DIR / poster_path)

            logger.debug(f"Saving {sponsor.slug!r} ({len(account_ids)} members)")
            Sponsor.create(
                tier=tier,
                subscription_id=subscription_id,
                start_on=start_on,
                renews_on=renews_on,
                note=note,
                logo_path=logo_path,
                poster_path=poster_path,
                account_ids=account_ids,
                **sponsor.model_dump(
                    exclude=["plan", "subscription", "note", "periods"]
                ),
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

    logger.debug("Resetting partners tables")
    db.drop_tables([Partner])
    db.create_tables([Partner])

    logger.info(f"Loading partners data from {PARTNERS_YAML_PATH}")
    partners_yaml_data = yaml.safe_load(PARTNERS_YAML_PATH.read_text())
    partners = PartnersConfig(**partners_yaml_data)
    default_plan_id = parse_plan_id(partners.default_plan)

    for partner in partners.registry:
        start_on = get_start_on([(partner.start_on, None)])
        if start_on > today:
            logger.warning(f"Future partner {partner.name} ({partner.slug})")
        else:
            logger.info(f"Partner {partner.name} ({partner.slug})")
            logger.debug("Checking plan and subscription")
            subscription_id = None
            account_ids = []
            if partner.plan:
                plan_id = parse_plan_id(partner.plan)
            elif partner.subscription:
                subscription_id = parse_subscription_id(partner.subscription)
                subscription = memberful.get(
                    SUBSCRIPTION_GQL_PATH.read_text(), dict(id=subscription_id)
                )["subscription"]
                plan_id = get_plan_id(subscription)
                account_ids = get_account_ids(subscription)
            else:
                plan_id = default_plan_id

            logger.debug(f"Checking logo for {sponsor.slug!r} exists")
            logo_path = find_logo(partner.slug)

            logger.debug(f"Saving {partner.slug!r} ({len(account_ids)} members)")
            Partner.create(
                subscription_id=subscription_id,
                plan_id=plan_id,
                start_on=start_on,
                logo_path=logo_path,
                note=parse_note(partner.note),
                account_ids=account_ids,
                **partner.model_dump(
                    exclude=["start_on", "plan", "subscription", "note"]
                ),
            )

    logger.info(f"Created {Partner.count()} partners")


def find_logo(slug: str) -> Path:
    logo_path = LOGOS_DIR / f"{slug}.svg"
    if not logo_path.exists():
        logo_path = logo_path.with_suffix(".png")
    if not logo_path.exists():
        raise FileNotFoundError(f"'There is no {slug}.svg or .png inside {LOGOS_DIR}")
    return logo_path.relative_to(IMAGES_DIR)


def get_plan_id(subscription: SubscriptionEntity) -> int:
    return int(subscription["plan"]["id"])


def get_account_ids(subscription: SubscriptionEntity) -> list[int]:
    if subscription["members"]["pageInfo"]["hasNextPage"]:
        raise NotImplementedError("Pagination not implemented")
    return [int(edge["node"]["id"]) for edge in subscription["members"]["edges"]]


def get_tier_data(plan: PlanEntity) -> dict[str, Any]:
    return dict(
        plan_id=int(plan["id"]),
        name=parse_tier_name(plan["name"]),
        price=from_cents(plan["priceCents"]),
        member_price=from_cents(plan["additionalMemberPriceCents"]) or None,
    )


def prepare_tiers(
    plans: Iterable[PlanEntity], extras: dict[str, dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    tiers = sorted(
        [
            get_tier_data(plan)
            for plan in plans
            if is_sponsor_plan(plan) and is_public_plan(plan)
        ],
        key=itemgetter("price"),
    )
    for tier_name, data in (extras or {}).items():
        try:
            tier = next((tier for tier in tiers if tier["name"] == tier_name))
            tier.update(data)
        except StopIteration:
            raise ValueError(f"Tier {tier_name!r} not found")
    return [dict(priority=priority, **data) for priority, data in enumerate(tiers)]


def get_start_on(periods: list[tuple[str, str | None]]) -> date:
    first_period_start = sorted(periods)[0][0]
    year, month = map(int, first_period_start.split("-"))
    return date(year, month, 1)


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


def check_css_integrity(tiers: Iterable[SponsorTier], css: str) -> None:
    tiers_priorities = {tier.priority for tier in tiers}
    css_priorities = set(map(int, LOGOS_CSS_RE.findall(css)))
    if tiers_priorities != css_priorities:
        raise ValueError(
            "Discrepancy between tier priorities and CSS: "
            f"{tiers_priorities!r} vs {css_priorities!r}"
        )


def parse_note(note: str | None) -> str | None:
    try:
        return note.strip() or None
    except AttributeError:
        return None


def parse_plan_id(plan_url: str | HttpUrl) -> int:
    return int(
        str(plan_url)
        .removeprefix("https://juniorguru.memberful.com/admin/plans/")
        .rstrip("/")
    )


def parse_subscription_id(subscription_url: str | HttpUrl) -> int:
    return int(
        str(subscription_url)
        .removeprefix("https://juniorguru.memberful.com/admin/subscriptions/")
        .rstrip("/")
    )
