from datetime import date
from numbers import Number
from typing import Any, Callable

from juniorguru.cli.sync import main as cli
from juniorguru.lib import charts, loggers
from juniorguru.lib.discord_club import DEFAULT_CHANNELS_HISTORY_SINCE
from juniorguru.models.base import db
from juniorguru.models.chart import Chart, ChartNamespace
from juniorguru.models.club import ClubMessage
from juniorguru.models.event import Event, EventSpeaking
from juniorguru.models.followers import Followers
from juniorguru.models.page import Page
from juniorguru.models.podcast import PodcastEpisode
from juniorguru.models.subscription import SubscriptionActivity, LEGACY_PLANS_DELETED_ON
from juniorguru.models.transaction import Transaction
from juniorguru.models.web_usage import WebUsage


BUSINESS_BEGIN_ON = date(2020, 1, 1)

CLUB_BEGIN_ON = date(2021, 2, 1)

PODCAST_BEGIN_ON = date(2022, 1, 1)

MILESTONES = [
    (BUSINESS_BEGIN_ON, 'Začátek podnikání'),
    (date(2020, 9, 1), 'Vznik příručky'),
    (CLUB_BEGIN_ON, 'Vznik klubu'),
    (PODCAST_BEGIN_ON, 'Vznik podcastu'),
    (date(2022, 9, 1), 'Zdražení firmám'),
    (date(2022, 12, 30), 'Zdražení členům'),
]

CHARTS = {}


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['transactions',
                                'subscriptions',
                                'members',
                                'pages',
                                'events',
                                'followers',
                                'club-content',
                                'podcast',
                                'web-usage'])
@db.connection_context()
def main():
    db.drop_tables([ChartNamespace, Chart])
    db.create_tables([ChartNamespace, Chart])

    today = date.today()
    for ns_slug, ns_data in CHARTS.items():
        logger.info(f'Generating namespace: {ns_slug}')
        meta_fn, charts = ns_data['meta'], ns_data['charts']
        meta = meta_fn(today)
        namespace = ChartNamespace.create(slug=ns_slug, **meta)
        for slug, chart_fn in charts.items():
            logger.info(f'Generating chart: {ns_slug}_{slug}')
            values = meta.get('values')
            data = chart_fn() if values is None else chart_fn(values)
            Chart.create(slug=slug, namespace=namespace, data=data)


def namespace(meta_fn: Callable) -> Callable:
    ns_slug = meta_fn.__name__
    if ns_slug in CHARTS:
        raise ValueError(f'Namespace {ns_slug!r} already registered')
    CHARTS[ns_slug] = dict(meta=meta_fn, charts={})
    return meta_fn


def chart(chart_fn: Callable) -> Callable:
    chart_fn_name = chart_fn.__name__
    try:
        ns_slug = sorted([ns_slug for ns_slug in CHARTS.keys()
                        if chart_fn_name.startswith(ns_slug)],
                        key=len, reverse=True)[0]
    except IndexError:
        raise ValueError(f'Could not find namespace for {chart_fn_name!r}')
    chart_slug = chart_fn_name.removeprefix(f'{ns_slug}_')
    try:
        CHARTS[ns_slug]['charts'][chart_slug] = chart_fn
    except KeyError:
        raise ValueError(f'Namespace {ns_slug!r} not registered')


@namespace
def business(today) -> dict[str, Any]:
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def business_profit(months: list[date]) -> list[Number]:
    return charts.per_month(Transaction.profit, months)


@chart
def business_profit_ttm(months: list[date]) -> list[Number]:
    return charts.per_month(Transaction.profit_ttm, months)


@chart
def business_revenue(months: list[date]) -> list[Number]:
    return charts.per_month(Transaction.revenue, months)


@chart
def business_revenue_ttm(months: list[date]) -> list[Number]:
    return charts.per_month(Transaction.revenue_ttm, months)


@chart
def business_revenue_breakdown(months: list[date]) -> list[Number]:
    return charts.per_month_breakdown(Transaction.revenue_breakdown, months)


@chart
def business_cost(months: list[date]) -> list[Number]:
    return charts.per_month(Transaction.cost, months)


@chart
def business_cost_ttm(months: list[date]) -> list[Number]:
    return charts.per_month(Transaction.cost_ttm, months)


@chart
def business_cost_breakdown(months: list[date]) -> list[Number]:
    return charts.per_month_breakdown(Transaction.cost_breakdown, months)


@namespace
def events(today) -> dict[str, Any]:
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def events_count(months: list[date]) -> list[Number]:
    return charts.per_month(Event.count_by_month, months)


@chart
def events_count_ttm(months: list[date]) -> list[Number]:
    return charts.per_month(Event.count_by_month_ttm, months)


@chart
def events_women_ptc_ttm(months: list[date]) -> list[Number]:
    return charts.per_month(EventSpeaking.women_ptc_ttm, months)


@namespace
def podcast(today) -> dict[str, Any]:
    months = charts.months(PODCAST_BEGIN_ON, today)
    return dict(values=months,
                labels=charts.labels(months))


@chart
def podcast_women_ptc_ttm(months: list[date]) -> list[Number]:
    return charts.per_month(PodcastEpisode.women_ptc_ttm, months)


@namespace
def members(today) -> dict[str, Any]:
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def members_all(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.active_count, months)


@chart
def members_individuals(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.active_individuals_count, months)


@chart
def members_individuals_yearly(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.active_individuals_yearly_count, months)


@chart
def members_women_ptc(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.active_women_ptc, months)


# @chart
# def members_duration(months: list[date]) -> list[Number]:
#     return charts.per_month(SubscriptionActivity.active_duration_avg, months)


@namespace
def members_subscriptions(today) -> dict[str, Any]:
    months = charts.months(charts.next_month(LEGACY_PLANS_DELETED_ON), today)
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def members_subscriptions_breakdown(months: list[date]) -> list[Number]:
    return charts.per_month_breakdown(SubscriptionActivity.active_subscription_type_breakdown, months)


@namespace
def members_trend(today) -> dict[str, Any]:
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def members_trend_signups(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.signups_count, months)


@chart
def members_trend_individuals_signups(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.individuals_signups_count, months)


@chart
def members_trend_quits(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.quits_count, months)


@chart
def members_trend_individuals_quits(months: list[date]) -> list[Number]:
    return charts.per_month(SubscriptionActivity.individuals_quits_count, months)


# @chart
# def members_trend_churn_ptc(months: list[date]) -> list[Number]:
#     return charts.per_month(SubscribedPeriod.churn_ptc, months)


# @chart
# def members_trend_individuals_churn_ptc(months: list[date]) -> list[Number]:
#     return charts.per_month(SubscribedPeriod.individuals_churn_ptc, months)


@namespace
def club_content(today) -> dict[str, Any]:
    months = charts.months(charts.next_month(today - DEFAULT_CHANNELS_HISTORY_SINCE), charts.previous_month(today))
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def club_content_size(months: list[date]) -> list[Number]:
    return charts.per_month(ClubMessage.content_size_by_month, months)


@namespace
def handbook(today) -> dict[str, Any]:
    return dict(labels=[f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
                        for page in Page.handbook_listing()])


@chart
def handbook_size() -> list[Number]:
    return [page.size for page in Page.handbook_listing()]


@chart
def handbook_notes_size() -> list[Number]:
    return [page.notes_size for page in Page.handbook_listing()]


@namespace
def followers(today) -> dict[str, Any]:
    months = charts.months(*Followers.months_range())
    return dict(values=months,
                labels=charts.labels(months))


@chart
def followers_breakdown(months: list[date]) -> list[Number]:
    return charts.per_month_breakdown(Followers.breakdown, months)


@namespace
def web_usage(today) -> dict[str, Any]:
    months = charts.months(*WebUsage.months_range())
    return dict(values=months,
                labels=charts.labels(months),
                annotations=charts.annotations(months, MILESTONES))


@chart
def web_usage_total(months: list[date]) -> list[Number]:
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    return breakdown.pop('total')


@chart
def web_usage_breakdown(months: list[date]) -> list[Number]:
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    del breakdown['total']
    return breakdown
