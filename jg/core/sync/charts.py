from datetime import date
from typing import Callable

from jg.core.cli.sync import main as cli
from jg.core.lib import charts, loggers
from jg.core.lib.discord_club import DEFAULT_CHANNELS_HISTORY_SINCE
from jg.core.models.base import db
from jg.core.models.chart import Chart
from jg.core.models.club import ClubMessage
from jg.core.models.event import Event, EventSpeaking
from jg.core.models.exchange_rate import ExchangeRate
from jg.core.models.followers import Followers
from jg.core.models.page import Page
from jg.core.models.podcast import PodcastEpisode
from jg.core.models.subscription import (
    LEGACY_PLANS_DELETED_ON,
    SubscriptionActivity,
    SubscriptionCancellation,
    SubscriptionCountry,
    SubscriptionInternalReferrer,
    SubscriptionMarketingSurvey,
    SubscriptionReferrer,
)
from jg.core.models.transaction import Transaction
from jg.core.models.web_usage import WebUsage


BUSINESS_BEGIN_ON = date(2020, 1, 1)

CLUB_BEGIN_ON = date(2021, 2, 1)

PODCAST_BEGIN_ON = date(2022, 1, 1)

SURVEYS_BEGIN_ON = date(2023, 1, 1)

MILESTONES = [
    (BUSINESS_BEGIN_ON, "Začátek podnikání"),
    (date(2020, 9, 1), "Vznik příručky"),
    (CLUB_BEGIN_ON, "Vznik klubu"),
    (PODCAST_BEGIN_ON, "Vznik podcastu"),
    (date(2022, 9, 1), "Zdražení firmám"),
    (date(2022, 12, 30), "Zdražení členům"),
    (date(2023, 5, 1), "Vznik kurzů"),
    (date(2023, 8, 31), "Restart newsletteru"),
]

CHARTS = {}


logger = loggers.from_path(__file__)


@cli.sync_command(
    dependencies=[
        "club-content",
        "events",
        "exchange-rates",
        "followers",
        "members",
        "pages",
        "podcast",
        "subscriptions-country",
        "subscriptions",
        "transactions",
        "web-usage",
    ]
)
@db.connection_context()
def main():
    Chart.drop_table()
    Chart.create_table()

    today = date.today()
    for chart_slug, chart_fn in CHARTS.items():
        logger.info(f"Generating: {chart_slug}")
        try:
            chart = chart_fn(today)
            chart.setdefault("slug", chart_slug)
            try:
                months = chart.pop("months")
            except KeyError:
                pass
            else:
                chart.setdefault("labels", charts.labels(months))
                chart.setdefault("annotations", charts.milestones(months, MILESTONES))
            Chart.create(**chart)
        except Exception:
            logger.exception(f"Failed to generate: {chart_slug}")


def chart(chart_fn: Callable) -> Callable:
    CHARTS[chart_fn.__name__] = chart_fn


@chart
def profit(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.profit, months)
    return dict(data=data, months=months)


@chart
def profit_ttm(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.profit_ttm, months)
    return dict(data=data, months=months)


@chart
def revenue(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.revenue, months)
    return dict(data=data, months=months)


@chart
def revenue_ttm(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.revenue_ttm, months)
    return dict(data=data, months=months)


@chart
def revenue_breakdown(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month_breakdown(Transaction.revenue_breakdown, months)
    return dict(data=data, months=months)


@chart
def cost(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.cost, months)
    return dict(data=data, months=months)


@chart
def cost_ttm(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.cost_ttm, months)
    return dict(data=data, months=months)


@chart
def cost_breakdown(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month_breakdown(Transaction.cost_breakdown, months)
    return dict(data=data, months=months)


@chart
def events(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(Event.count_by_month, months)
    return dict(data=data, months=months)


@chart
def events_ttm(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(Event.count_by_month_ttm, months)
    return dict(data=data, months=months)


@chart
def events_women(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(EventSpeaking.women_ptc_ttm, months)
    return dict(data=data, months=months)


@chart
def podcast_women(today: date):
    months = charts.months(PODCAST_BEGIN_ON, today)
    data = charts.per_month(PodcastEpisode.women_ptc_ttm, months)
    return dict(data=data, months=months)


@chart
def members(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(SubscriptionActivity.active_count, months)
    return dict(data=data, months=months)


@chart
def members_individuals(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(SubscriptionActivity.active_individuals_count, months)
    return dict(data=data, months=months)


@chart
def members_individuals_yearly(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(
        SubscriptionActivity.active_individuals_yearly_count, months
    )
    return dict(data=data, months=months)


@chart
def members_women(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(SubscriptionActivity.active_women_ptc, months)
    return dict(data=data, months=months)


@chart
def subscriptions_duration(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(SubscriptionActivity.active_duration_avg, months)
    return dict(data=data, months=months)


@chart
def subscriptions_duration_individuals(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(
        SubscriptionActivity.active_individuals_duration_avg, months
    )
    return dict(data=data, months=months)


@chart
def total_marketing_breakdown(today: date):
    return dict(
        data=SubscriptionMarketingSurvey.total_breakdown_ptc(),
        count=SubscriptionMarketingSurvey.count(),
    )


@chart
def total_spend_marketing_breakdown(today: date):
    return dict(
        data=SubscriptionMarketingSurvey.total_spend_breakdown_ptc(),
        count=SubscriptionMarketingSurvey.count(),
    )


@chart
def total_referrer_breakdown(today: date):
    return dict(
        data=SubscriptionReferrer.total_breakdown_ptc(),
        count=SubscriptionReferrer.count(),
    )


@chart
def total_spend_referrer_breakdown(today: date):
    return dict(
        data=SubscriptionReferrer.total_spend_breakdown_ptc(),
        count=SubscriptionReferrer.count(),
    )


@chart
def total_internal_referrer_breakdown(today: date):
    period_days = 30 * 6
    return dict(
        data=SubscriptionInternalReferrer.total_breakdown_ptc(period_days),
        count=SubscriptionInternalReferrer.count(period_days),
    )


@chart
def total_spend_internal_referrer_breakdown(today: date):
    period_days = 30 * 6
    return dict(
        data=SubscriptionInternalReferrer.total_spend_breakdown_ptc(period_days),
        count=SubscriptionInternalReferrer.count(period_days),
    )


@chart
def cancellations_breakdown(today: date):
    months = charts.months(SURVEYS_BEGIN_ON, today)
    data = charts.per_month_breakdown(SubscriptionCancellation.breakdown_ptc, months)
    count = SubscriptionCancellation.count()
    return dict(data=data, months=months, count=count)


@chart
def total_cancellations_breakdown(today: date):
    return dict(
        data=SubscriptionCancellation.total_breakdown_ptc(),
        count=SubscriptionCancellation.count(),
    )


@chart
def subscriptions_breakdown(today: date):
    months = charts.months(charts.next_month(LEGACY_PLANS_DELETED_ON), today)
    data = charts.per_month_breakdown(
        SubscriptionActivity.active_subscription_type_breakdown, months
    )
    return dict(data=data, months=months)


@chart
def trials_conversion(today: date):
    months = charts.months(
        charts.next_month(LEGACY_PLANS_DELETED_ON), charts.previous_month(today)
    )
    data = charts.per_month(SubscriptionActivity.trial_conversion_ptc, months)
    return dict(data=data, months=months)


@chart
def signups(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    data = charts.per_month(SubscriptionActivity.signups_count, months)
    return dict(data=data, months=months)


@chart
def signups_individuals(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    data = charts.per_month(SubscriptionActivity.individuals_signups_count, months)
    return dict(data=data, months=months)


@chart
def quits(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    data = charts.per_month(SubscriptionActivity.quits_count, months)
    return dict(data=data, months=months)


@chart
def quits_individuals(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    data = charts.per_month(SubscriptionActivity.individuals_quits_count, months)
    return dict(data=data, months=months)


@chart
def churn(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    data = charts.per_month(SubscriptionActivity.churn_ptc, months)
    return dict(data=data, months=months)


@chart
def churn_individuals(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    data = charts.per_month(SubscriptionActivity.individuals_churn_ptc, months)
    return dict(data=data, months=months)


@chart
def club_content(today: date):
    months = charts.months(
        charts.next_month(today - DEFAULT_CHANNELS_HISTORY_SINCE),
        charts.previous_month(today),
    )
    data = charts.per_month(ClubMessage.content_size_by_month, months)
    return dict(data=data, months=months)


@chart
def handbook(today: date):
    labels = [
        f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
        for page in Page.handbook_listing()
    ]
    data = [page.size for page in Page.handbook_listing()]
    return dict(data=data, labels=labels)


@chart
def handbook_notes(today: date):
    labels = [
        f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
        for page in Page.handbook_listing()
    ]
    data = [page.notes_size for page in Page.handbook_listing()]
    return dict(data=data, labels=labels)


@chart
def followers_breakdown(today: date):
    months = charts.months(*Followers.months_range())
    data = charts.per_month_breakdown(Followers.breakdown, months)
    return dict(data=data, months=months)


@chart
def web_usage_total(today: date):
    months = charts.months(*WebUsage.months_range())
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    return dict(data=breakdown.pop("total"), months=months)


@chart
def web_usage_breakdown(today: date):
    months = charts.months(*WebUsage.months_range())
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    del breakdown["total"]
    return dict(data=breakdown, months=months)


@chart
def countries(today: date):
    breakdown = SubscriptionCountry.total_breakdown_ptc()

    oss_limit_eur = 10000
    oss_limit_czk = ExchangeRate.from_currency(oss_limit_eur, "EUR")

    revenue_breakdown = Transaction.revenue_breakdown(charts.previous_month(today))
    revenue_memberships = revenue_breakdown["memberships"]

    return dict(
        data=dict(
            breakdown=breakdown,
            oss_limit_eur=oss_limit_eur,
            oss_limit_czk=oss_limit_czk,
            oss_limit_czk_monthly=int(oss_limit_czk / 12),
            revenue_memberships=revenue_memberships,
            revenue_memberships_non_cz=int(
                ((100 - breakdown["CZ"]) * revenue_memberships) / 100
            ),
        )
    )
