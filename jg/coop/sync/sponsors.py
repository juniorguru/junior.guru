from datetime import date, timedelta
from pathlib import Path

import click
import yaml
from pydantic import BaseModel, HttpUrl

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.sponsor import PastSponsor, Sponsor, SponsorTier


YAML_PATH = Path("jg/coop/data/sponsors.yml")


logger = loggers.from_path(__file__)


class TierConfig(BaseModel):
    slug: str


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
@db.connection_context()
def main(today: date):
    db.drop_tables([Sponsor, SponsorTier, PastSponsor])
    db.create_tables([Sponsor, SponsorTier, PastSponsor])

    yaml_data = yaml.safe_load(YAML_PATH.read_text())
    sponsors = SponsorsConfig(**yaml_data)

    tiers = {tier.slug: SponsorTier.create(slug=tier.slug) for tier in sponsors.tiers}
    logger.info(f"Tiers: {', '.join(tiers.keys())}")

    for sponsor in sponsors.registry:
        if renews_on := renew_date(sponsor.periods, today):
            logger.info(f"Sponsor {sponsor.name} ({sponsor.slug})")
            Sponsor.create(
                slug=sponsor.slug,
                name=sponsor.name,
                url=sponsor.url,
                tier=tiers[sponsor.tier] if sponsor.tier else None,
                renews_on=renews_on,
            )
        else:
            logger.info(f"Past sponsor {sponsor.name} ({sponsor.slug})")
            PastSponsor.create(
                slug=sponsor.slug,
                name=sponsor.name,
                url=sponsor.url,
            )

    logger.info(
        f"Created {Sponsor.count()} sponsors and {PastSponsor.count()} past sponsors"
    )


def renew_date(periods: list[tuple[str, str | None]], today: date) -> bool:
    current_period = sorted(periods, reverse=True)[0]
    period_start, period_end = current_period

    if period_end:
        year, month = map(int, period_end.split("-"))
        renew_date = next_month(date(year, month, 1))
        return None if renew_date < today else renew_date

    month = int(period_start.split("-")[1])
    if date(today.year, month, 1) < today.replace(day=1):
        return next_month(date(today.year + 1, month, 1))

    return next_month(date(today.year, month, 1))


def next_month(month: date) -> date:
    return (month.replace(day=1) + timedelta(days=32)).replace(day=1)
