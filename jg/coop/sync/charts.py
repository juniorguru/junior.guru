from datetime import date
from typing import Any, Callable, NotRequired, TypedDict

from jg.coop.cli.sync import main as cli
from jg.coop.lib import charts, loggers
from jg.coop.lib.discord_club import DEFAULT_CHANNELS_HISTORY_SINCE
from jg.coop.models.base import db
from jg.coop.models.chart import Chart
from jg.coop.models.club import ClubMessage
from jg.coop.models.event import Event, EventSpeaking
from jg.coop.models.exchange_rate import ExchangeRate
from jg.coop.models.followers import Followers
from jg.coop.models.members import Members
from jg.coop.models.page import Page
from jg.coop.models.podcast import PodcastEpisode
from jg.coop.models.subscription import (
    SubscriptionCancellation,
    SubscriptionCountry,
    SubscriptionInternalReferrer,
    SubscriptionMarketingSurvey,
    SubscriptionReferrer,
)
from jg.coop.models.transaction import Transaction
from jg.coop.models.web_usage import WebUsage


BUSINESS_BEGIN_ON = date(2020, 1, 1)

CLUB_BEGIN_ON = date(2021, 2, 1)

PODCAST_BEGIN_ON = date(2022, 1, 1)

SURVEYS_BEGIN_ON = date(2023, 1, 1)

MEMBERS_DATA_BEGIN_ON = date(2024, 7, 1)

MILESTONES = [
    (BUSINESS_BEGIN_ON, "Začátek podnikání"),
    (date(2020, 9, 1), "Vznik příručky"),
    (CLUB_BEGIN_ON, "Vznik klubu"),
    (PODCAST_BEGIN_ON, "Vznik podcastu"),
    (date(2023, 5, 1), "Vznik kurzů"),
]

CHARTS = {}


logger = loggers.from_path(__file__)


class ChartDict(TypedDict):
    data: Any
    months: NotRequired[list[date]]
    labels: NotRequired[list[str]]
    count: NotRequired[int]


class IntChartDict(ChartDict):
    data: list[int]


class IntBreakdownChartDict(ChartDict):
    data: dict[str, int]


class FloatChartDict(ChartDict):
    data: list[float]


class FloatBreakdownChartDict(ChartDict):
    data: dict[str, float]


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
def profit(today: date) -> IntChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.profit, months)
    return dict(data=data, months=months)


@chart
def profit_ttm(today: date) -> IntChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.profit_ttm, months)
    return dict(data=data, months=months)


@chart
def revenue(today: date) -> IntChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.revenue, months)
    return dict(data=data, months=months)


@chart
def revenue_ttm(today: date) -> IntChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.revenue_ttm, months)
    return dict(data=data, months=months)


@chart
def revenue_breakdown(today: date) -> IntBreakdownChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month_breakdown(Transaction.revenue_breakdown, months)
    return dict(data=data, months=months)


@chart
def cost(today: date) -> IntChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.cost, months)
    return dict(data=data, months=months)


@chart
def cost_ttm(today: date) -> IntChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month(Transaction.cost_ttm, months)
    return dict(data=data, months=months)


@chart
def cost_breakdown(today: date) -> IntBreakdownChartDict:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    data = charts.per_month_breakdown(Transaction.cost_breakdown, months)
    return dict(data=data, months=months)


@chart
def events(today: date) -> IntChartDict:
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(Event.count_by_month, months)
    return dict(data=data, months=months)


@chart
def events_ttm(today: date) -> IntChartDict:
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(Event.count_by_month_ttm, months)
    return dict(data=data, months=months)


@chart
def events_women(today: date) -> FloatChartDict:
    months = charts.months(CLUB_BEGIN_ON, today)
    data = charts.per_month(EventSpeaking.women_ptc_ttm, months)
    return dict(data=data, months=months)


@chart
def podcast_women(today: date) -> FloatChartDict:
    months = charts.months(PODCAST_BEGIN_ON, today)
    data = charts.per_month(PodcastEpisode.women_ptc_ttm, months)
    return dict(data=data, months=months)


@chart
def members(today: date) -> IntChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_members(months)
    return dict(data=data, months=months)


@chart
def members_individuals(today: date) -> IntChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_members_individuals(months)
    return dict(data=data, months=months)


@chart
def members_individuals_today(today: date) -> ChartDict:
    data = Members.monthly_members_individuals([today])[-1]
    return dict(data=data)


@chart
def members_individuals_today_ptc(today: date) -> ChartDict:
    members_individuals_count = Members.monthly_members_individuals([today])[-1]
    members_count = Members.monthly_members([today])[-1]
    data = (members_individuals_count * 100) / members_count
    return dict(data=data)


@chart
def members_women(today: date) -> FloatChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_members_women_ptc(months)
    return dict(data=data, months=months)


@chart
def members_women_today(today: date) -> ChartDict:
    data = Members.monthly_members_women_ptc([today])[-1]
    return dict(data=data)


@chart
def total_marketing_breakdown(today: date) -> FloatBreakdownChartDict:
    return dict(
        data=SubscriptionMarketingSurvey.total_breakdown_ptc(),
        count=SubscriptionMarketingSurvey.count(),
    )


@chart
def total_spend_marketing_breakdown(today: date) -> FloatBreakdownChartDict:
    return dict(
        data=SubscriptionMarketingSurvey.total_spend_breakdown_ptc(),
        count=SubscriptionMarketingSurvey.count(),
    )


@chart
def total_referrer_breakdown(today: date) -> FloatBreakdownChartDict:
    return dict(
        data=SubscriptionReferrer.total_breakdown_ptc(),
        count=SubscriptionReferrer.count(),
    )


@chart
def total_spend_referrer_breakdown(today: date) -> FloatBreakdownChartDict:
    return dict(
        data=SubscriptionReferrer.total_spend_breakdown_ptc(),
        count=SubscriptionReferrer.count(),
    )


@chart
def total_internal_referrer_breakdown(today: date) -> FloatBreakdownChartDict:
    period_days = 30 * 6
    return dict(
        data=SubscriptionInternalReferrer.total_breakdown_ptc(period_days),
        count=SubscriptionInternalReferrer.count(period_days),
    )


@chart
def total_spend_internal_referrer_breakdown(today: date) -> FloatBreakdownChartDict:
    period_days = 30 * 6
    return dict(
        data=SubscriptionInternalReferrer.total_spend_breakdown_ptc(period_days),
        count=SubscriptionInternalReferrer.count(period_days),
    )


@chart
def cancellations_breakdown(today: date) -> IntBreakdownChartDict:
    months = charts.months(SURVEYS_BEGIN_ON, today)
    data = charts.per_month_breakdown(SubscriptionCancellation.breakdown_ptc, months)
    count = SubscriptionCancellation.count()
    return dict(data=data, months=months, count=count)


@chart
def total_cancellations_breakdown(today: date) -> FloatBreakdownChartDict:
    return dict(
        data=SubscriptionCancellation.total_breakdown_ptc(),
        count=SubscriptionCancellation.count(),
    )


@chart
def subscription_types_breakdown(today: date) -> IntBreakdownChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_subscription_types_breakdown(months)
    return dict(data=data, months=months)


@chart
def trials_conversion(today: date) -> FloatChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_converting_trials_ptc(months)
    return dict(data=data, months=months)


@chart
def signups(today: date) -> IntChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_signups(months)
    return dict(data=data, months=months)


@chart
def quits(today: date) -> IntChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_quits(months)
    return dict(data=data, months=months)


@chart
def churn(today: date) -> FloatChartDict:
    months = charts.months(MEMBERS_DATA_BEGIN_ON, today)
    data = Members.monthly_churn_ptc(months)
    return dict(data=data, months=months)


@chart
def club_content(today: date) -> IntChartDict:
    months = charts.months(
        charts.next_month(today - DEFAULT_CHANNELS_HISTORY_SINCE),
        charts.previous_month(today),
    )
    data = charts.per_month(ClubMessage.content_size_by_month, months)
    return dict(data=data, months=months)


@chart
def handbook(today: date) -> IntChartDict:
    labels = [
        f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
        for page in Page.handbook_listing()
    ]
    data = [page.size for page in Page.handbook_listing()]
    return dict(data=data, labels=labels)


@chart
def handbook_notes(today: date) -> IntChartDict:
    labels = [
        f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
        for page in Page.handbook_listing()
    ]
    data = [page.notes_size for page in Page.handbook_listing()]
    return dict(data=data, labels=labels)


@chart
def followers_breakdown(today: date) -> IntBreakdownChartDict:
    months = charts.months(*Followers.months_range())
    data = charts.per_month_breakdown(Followers.breakdown, months)
    return dict(data=data, months=months)


@chart
def web_usage_total(today: date) -> ChartDict:
    months = charts.months(*WebUsage.months_range())
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    return dict(data=breakdown.pop("total"), months=months)


@chart
def web_usage_breakdown(today: date) -> IntBreakdownChartDict:
    months = charts.months(*WebUsage.months_range())
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    del breakdown["total"]
    return dict(data=breakdown, months=months)


@chart
def web_club_conversion(today: date) -> FloatChartDict:
    start_on, end_on = WebUsage.months_range()
    start_on = max(start_on, MEMBERS_DATA_BEGIN_ON)
    months = charts.months(start_on, end_on)
    data = [
        (
            (count_trials / count_visits) * 100
            if (count_trials is not None and count_visits)
            else None
        )
        for (count_trials, count_visits) in zip(
            Members.monthly_trials(months),
            [WebUsage.breakdown(month).get("club") for month in months],
        )
    ]
    return dict(data=data, months=months)


@chart
def logo_impressions_breakdown(today: date) -> IntBreakdownChartDict:
    product_names = ["home", "courses", "handbook"]
    months = charts.months(*WebUsage.months_range())
    months_len = len(months)
    web_usage_breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    web_usage_breakdown_items = sorted(
        web_usage_breakdown.items(), key=lambda item: position(product_names, item[0])
    )
    impressions_breakdown = {
        product_name: int(sum(values) / months_len)
        for product_name, values in web_usage_breakdown_items
        if product_name in product_names
    }
    return dict(data=impressions_breakdown)


def position(names: list[str], name: str):
    try:
        return names.index(name)
    except ValueError:
        return len(names)


@chart
def countries(today: date) -> ChartDict:
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
