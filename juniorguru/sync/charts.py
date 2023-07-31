from datetime import date
from typing import Callable

from juniorguru.cli.sync import main as cli
from juniorguru.lib import charts, loggers
from juniorguru.lib.discord_club import DEFAULT_CHANNELS_HISTORY_SINCE
from juniorguru.models.base import db
from juniorguru.models.chart import Chart
from juniorguru.models.club import ClubMessage
from juniorguru.models.event import Event, EventSpeaking
from juniorguru.models.followers import Followers
from juniorguru.models.page import Page
from juniorguru.models.podcast import PodcastEpisode
from juniorguru.models.subscription import (LEGACY_PLANS_DELETED_ON,
                                            SubscriptionActivity,
                                            SubscriptionCancellation,
                                            SubscriptionMarketingSurvey)
from juniorguru.models.transaction import Transaction
from juniorguru.models.web_usage import WebUsage


BUSINESS_BEGIN_ON = date(2020, 1, 1)

CLUB_BEGIN_ON = date(2021, 2, 1)

PODCAST_BEGIN_ON = date(2022, 1, 1)

SURVEYS_BEGIN_ON = date(2023, 1, 1)

MILESTONES = [
    (BUSINESS_BEGIN_ON, 'Začátek podnikání'),
    (date(2020, 9, 1), 'Vznik příručky'),
    (CLUB_BEGIN_ON, 'Vznik klubu'),
    (PODCAST_BEGIN_ON, 'Vznik podcastu'),
    (date(2022, 9, 1), 'Zdražení firmám'),
    (date(2022, 12, 30), 'Zdražení členům'),
    (date(2023, 5, 1), 'Vznik katalogu kurzů'),
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
    Chart.drop_table()
    Chart.create_table()

    today = date.today()
    for chart_slug, chart_fn in CHARTS.items():
        logger.info(f'Generating: {chart_slug}')
        Chart.create(**chart_fn(today))


def chart(chart_fn: Callable) -> Callable:
    CHARTS[chart_fn.__name__] = chart_fn


@chart
def business_profit(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month(Transaction.profit, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_profit_ttm(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month(Transaction.profit_ttm, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_revenue(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month(Transaction.revenue, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_revenue_ttm(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month(Transaction.revenue_ttm, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_revenue_breakdown(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month_breakdown(Transaction.revenue_breakdown, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_cost(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month(Transaction.cost, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_cost_ttm(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month(Transaction.cost_ttm, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def business_cost_breakdown(today: date):
    months = charts.months(BUSINESS_BEGIN_ON, today)
    return dict(data=charts.per_month_breakdown(Transaction.cost_breakdown, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def events_count(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(Event.count_by_month, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def events_count_ttm(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(Event.count_by_month_ttm, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def events_women_ptc_ttm(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(EventSpeaking.women_ptc_ttm, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def podcast_women_ptc_ttm(today: date):
    months = charts.months(PODCAST_BEGIN_ON, today)
    return dict(data=charts.per_month(PodcastEpisode.women_ptc_ttm, months),
                labels=charts.labels(months))


@chart
def members_all(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(SubscriptionActivity.active_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_individuals(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(SubscriptionActivity.active_individuals_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_individuals_yearly(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(SubscriptionActivity.active_individuals_yearly_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_women_ptc(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(SubscriptionActivity.active_women_ptc, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_duration(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(SubscriptionActivity.active_duration_avg, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_individuals_duration(today: date):
    months = charts.months(CLUB_BEGIN_ON, today)
    return dict(data=charts.per_month(SubscriptionActivity.active_individuals_duration_avg, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_surveys_cancellations_breakdown(today: date):
    months = charts.months(SURVEYS_BEGIN_ON, today)
    return dict(data=charts.per_month_breakdown(SubscriptionCancellation.breakdown_ptc, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_surveys_marketing_breakdown(today: date):
    months = charts.months(SURVEYS_BEGIN_ON, today)
    return dict(data=charts.per_month_breakdown(SubscriptionMarketingSurvey.breakdown_ptc, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_surveys_total_cancellations_breakdown(today: date):
    return dict(data=SubscriptionCancellation.total_breakdown_ptc())


@chart
def members_surveys_total_marketing_breakdown(today: date):
    return dict(data=SubscriptionMarketingSurvey.total_breakdown_ptc())


@chart
def members_surveys_total_spend_marketing_breakdown(today: date):
    return dict(data=SubscriptionMarketingSurvey.total_spend_breakdown_ptc())


@chart
def members_subscriptions_breakdown(today: date):
    months = charts.months(charts.next_month(LEGACY_PLANS_DELETED_ON), today)
    return dict(data=charts.per_month_breakdown(SubscriptionActivity.active_subscription_type_breakdown, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_subscriptions_trial_conversion(today: date):
    months = charts.months(charts.next_month(LEGACY_PLANS_DELETED_ON),
                           charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.trial_conversion_ptc, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_trend_signups(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.signups_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_trend_individuals_signups(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.individuals_signups_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_trend_quits(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.quits_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_trend_individuals_quits(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.individuals_quits_count, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_trend_churn_ptc(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.churn_ptc, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def members_trend_individuals_churn_ptc(today: date):
    months = charts.months(CLUB_BEGIN_ON, charts.previous_month(today))
    return dict(data=charts.per_month(SubscriptionActivity.individuals_churn_ptc, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def club_content_size(today: date):
    months = charts.months(charts.next_month(today - DEFAULT_CHANNELS_HISTORY_SINCE),
                           charts.previous_month(today))
    return dict(data=charts.per_month(ClubMessage.content_size_by_month, months),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def handbook_size(today: date):
    labels = [f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
              for page in Page.handbook_listing()]
    return dict(data=[page.size for page in Page.handbook_listing()],
                labels=labels)


@chart
def handbook_notes_size(today: date):
    labels = [f"{page.meta['emoji']} {page.src_uri.removeprefix('handbook/')}"
              for page in Page.handbook_listing()]
    return dict(data=[page.notes_size for page in Page.handbook_listing()],
                labels=labels)


@chart
def followers_breakdown(today: date):
    months = charts.months(*Followers.months_range())
    return dict(data=charts.per_month_breakdown(Followers.breakdown, months),
                labels=charts.labels(months))


@chart
def web_usage_total(today: date):
    months = charts.months(*WebUsage.months_range())
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    return dict(data=breakdown.pop('total'),
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))


@chart
def web_usage_breakdown(today: date):
    months = charts.months(*WebUsage.months_range())
    breakdown = charts.per_month_breakdown(WebUsage.breakdown, months)
    del breakdown['total']
    return dict(data=breakdown,
                labels=charts.labels(months),
                annotations=charts.milestones(months, MILESTONES))
