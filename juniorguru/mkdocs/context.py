import hashlib
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import arrow

from juniorguru.lib import charts
from juniorguru.lib.club import DEFAULT_CHANNELS_HISTORY_SINCE
from juniorguru.mkdocs.thumbnail import thumbnail
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubSubscribedPeriod, ClubUser
from juniorguru.models.event import Event, EventSpeaking
from juniorguru.models.job import ListedJob
from juniorguru.models.partner import Partner
from juniorguru.models.podcast import PodcastEpisode
from juniorguru.models.story import Story
from juniorguru.models.topic import Topic
from juniorguru.models.transaction import Transaction
from juniorguru.lib.benefits_evaluators import BENEFITS_EVALUATORS


NOW = arrow.utcnow()

TODAY = NOW.date()

BUSINESS_BEGIN_ON = date(2020, 1, 1)

CLUB_BEGIN_ON = date(2021, 2, 1)

MILESTONES = [
    (BUSINESS_BEGIN_ON, 'Začátek podnikání'),
    (date(2020, 9, 1), 'Vznik příručky'),
    (CLUB_BEGIN_ON, 'Vznik klubu'),
    (date(2022, 1, 1), 'Vznik podcastu'),
    (date(2022, 9, 1), 'Zdražení firmám'),
    (date(2022, 12, 30), 'Zdražení členům'),
]

CLOUDINARY_HOST = os.getenv('CLOUDINARY_HOST', 'res.cloudinary.com')


####################################################################
# SHARED DOCS AND THEME CONTEXT                                    #
####################################################################


@db.connection_context()
def on_shared_context(context):
    context['now'] = NOW
    context['today'] = TODAY
    context['profit_ttm'] = Transaction.profit_ttm(TODAY)
    context['revenue_ttm_breakdown'] = Transaction.revenue_ttm_breakdown(TODAY)
    context['cloudinary_host'] = CLOUDINARY_HOST


def on_shared_page_context(context, page, config, files):
    pass


####################################################################
# DOCS CONTEXT                                                     #
####################################################################


@db.connection_context()
def on_docs_context(context):
    # topics/*
    context['club_elapsed_months'] = int(round((TODAY - CLUB_BEGIN_ON).days / 30))
    context['members'] = ClubUser.avatars_listing()
    context['members_total_count'] = ClubUser.members_count()

    # club.md
    context['finaid_url'] = 'https://docs.google.com/forms/d/e/1FAIpQLSeJ_Bmq__X8AA-XbKqU-Vr1N6fdGHSBQ-IuneO5zhBcGCOgjQ/viewform?usp=sf_link'
    context['messages_count'] = ClubMessage.count()
    context['partners'] = Partner.active_listing()  # also open.md
    context['partners_schools'] = Partner.active_schools_listing()
    context['events'] = Event.listing()
    context['events_club'] = Event.club_listing()

    # handbook/motivation.md
    context['stories'] = Story.listing()
    context['stories_by_tags'] = Story.tags_mapping()

    # handbook/candidate.md
    context['jobs'] = ListedJob.listing()
    context['jobs_remote'] = ListedJob.remote_listing()
    context['jobs_internship'] = ListedJob.internship_listing()
    context['jobs_volunteering'] = ListedJob.volunteering_listing()

    # open.md
    context['partners_expired'] = Partner.expired_listing()
    business_charts_months = charts.months(BUSINESS_BEGIN_ON, TODAY)
    context['charts_business_labels'] = charts.labels(business_charts_months)
    context['charts_business_annotations'] = charts.annotations(business_charts_months, MILESTONES)
    context['charts_profit'] = charts.per_month(Transaction.profit, business_charts_months)
    context['charts_profit_ttm'] = charts.per_month(Transaction.profit_ttm, business_charts_months)
    context['charts_revenue'] = charts.per_month(Transaction.revenue, business_charts_months)
    context['charts_revenue_ttm'] = charts.per_month(Transaction.revenue_ttm, business_charts_months)
    context['charts_revenue_breakdown'] = charts.per_month_breakdown(Transaction.revenue_breakdown, business_charts_months)
    context['charts_cost'] = charts.per_month(Transaction.cost, business_charts_months)
    context['charts_cost_ttm'] = charts.per_month(Transaction.cost_ttm, business_charts_months)
    context['charts_cost_breakdown'] = charts.per_month_breakdown(Transaction.cost_breakdown, business_charts_months)
    club_charts_months = charts.months(CLUB_BEGIN_ON, TODAY)
    context['charts_club_labels'] = charts.labels(club_charts_months)
    context['charts_club_annotations'] = charts.annotations(club_charts_months, MILESTONES)
    context['charts_subscriptions'] = charts.per_month(ClubSubscribedPeriod.count, club_charts_months)
    context['charts_individuals'] = charts.per_month(ClubSubscribedPeriod.individuals_count, club_charts_months)
    context['charts_individuals_yearly'] = charts.per_month(ClubSubscribedPeriod.individuals_yearly_count, club_charts_months)
    context['charts_subscriptions_breakdown'] = charts.per_month_breakdown(ClubSubscribedPeriod.count_breakdown, club_charts_months)
    context['charts_women_ptc'] = charts.per_month(ClubSubscribedPeriod.women_ptc, club_charts_months)
    context['charts_individuals_duration'] = charts.per_month(ClubSubscribedPeriod.individuals_duration_avg, club_charts_months)
    club_trend_charts_months = charts.months(CLUB_BEGIN_ON, charts.previous_month(TODAY))
    context['charts_club_trend_labels'] = charts.labels(club_trend_charts_months)
    context['charts_signups'] = charts.per_month(ClubSubscribedPeriod.signups_count, club_trend_charts_months)
    context['charts_individuals_signups'] = charts.per_month(ClubSubscribedPeriod.individuals_signups_count, club_trend_charts_months)
    context['charts_churn_ptc'] = charts.per_month(ClubSubscribedPeriod.churn_ptc, club_trend_charts_months)
    context['charts_individuals_churn_ptc'] = charts.per_month(ClubSubscribedPeriod.individuals_churn_ptc, club_trend_charts_months)
    club_messages_charts_months = charts.months(charts.next_month(TODAY - DEFAULT_CHANNELS_HISTORY_SINCE), charts.previous_month(TODAY))
    context['charts_club_messages_labels'] = charts.labels(club_messages_charts_months)
    context['charts_club_messages_annotations'] = charts.annotations(club_messages_charts_months, MILESTONES)
    context['charts_messages'] = charts.per_month(ClubMessage.count_by_month, club_messages_charts_months)
    context['charts_events'] = charts.per_month(Event.count_by_month, club_charts_months)
    context['charts_events_ttm'] = charts.per_month(Event.count_by_month_ttm, club_charts_months)
    context['charts_events_women_ptc_ttm'] = charts.per_month(EventSpeaking.women_ptc_ttm, club_charts_months)

    # open/*
    context['benefits_evaluators'] = BENEFITS_EVALUATORS

    # podcast.md, handbook/cv.md
    context['podcast_episodes'] = PodcastEpisode.listing()


@db.connection_context()
def on_docs_page_context(context, page, config, files):
    meta_model_getters = (
        ('topic_name', Topic.get_by_id, 'topic'),
        ('partner_slug', Partner.get_by_slug, 'partner'),
    )
    for meta_key, model_getter, model_var in meta_model_getters:
        if meta_key in page.meta:
            context[model_var] = model_getter(page.meta[meta_key])


####################################################################
# THEME CONTEXT                                                    #
####################################################################


def on_theme_context(context):
    js_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle.js'
    css_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle-mkdocs.css'
    context['js_hash'] = hash_file(js_path)
    context['css_hash'] = hash_file(css_path)
    context['bootstrap_icons_file'] = re.search(r'bootstrap-icons.woff2\?\w+', css_path.read_text()).group(0)

    context['partners_handbook'] = Partner.handbook_listing()


@db.connection_context()
def on_theme_page_context(context, page, config, files):
    page.meta.setdefault('title', 'Jak se naučit programovat a získat první práci v IT')

    thumbnail_path = thumbnail(page.meta.get('thumbnail_title', page.meta['title']),
                               badge=page.meta.get('thumbnail_badge'))
    context['thumbnail_url'] = urljoin(config['site_url'], f'static/{thumbnail_path}')

    context['parent_page'] = get_parent_page(page)
    context['previous_page'] = get_sibling_page(page, -1)
    context['next_page'] = get_sibling_page(page, +1)


####################################################################
# HELPER FUNCTIONS                                                 #
####################################################################


def hash_file(path):
    hash = hashlib.sha512()
    hash.update(path.read_bytes())
    return hash.hexdigest()


def get_parent_page(page):
    try:
        return page.parent.children[0]
    except AttributeError:
        return None


def get_sibling_page(page, offset):
    try:
        index = page.parent.children.index(page)
        sibling_index = max(index + offset, 0)
        if index == sibling_index:
            return None
        return page.parent.children[sibling_index]
    except (AttributeError, IndexError):
        return None
