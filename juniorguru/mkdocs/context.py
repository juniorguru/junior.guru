import re
import hashlib
from pathlib import Path
from urllib.parse import urljoin
from datetime import date

import arrow

from juniorguru.lib import charts
from juniorguru.models import db, Topic, ClubUser, Company, Event, ClubMessage, Story, LastModified, ListedJob, Transaction, PodcastEpisode
from juniorguru.mkdocs.thumbnail import thumbnail


NOW = arrow.utcnow()
TODAY = NOW.date()
BUSINESS_BEGIN_ON = date(2020, 1, 1)
CLUB_BEGIN_ON = date(2021, 2, 1)


####################################################################
# SHARED DOCS AND THEME CONTEXT                                    #
####################################################################


@db.connection_context()
def on_shared_context(context):
    context['now'] = NOW
    context['today'] = TODAY
    context['profit_ttm'] = Transaction.profit_ttm(TODAY)
    context['revenue_ttm_breakdown'] = Transaction.revenue_ttm_breakdown(TODAY)
    context['pricing_url'] = 'https://docs.google.com/document/d/1keFyO5aavfaNfJkKlyYha4B-UbdnMja6AhprS_76E7c/'


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
    context['companies'] = Company.listing()
    context['companies_students'] = Company.students_listing()
    context['events'] = Event.listing()

    # motivation.md
    context['stories'] = Story.listing()
    context['stories_by_tags'] = Story.tags_mapping()

    # candidate-handbook.md
    context['last_modified'] = LastModified.get_value_by_path('candidate-handbook.md')
    context['jobs'] = []  # TODO ListedJob.listing()
    context['jobs_remote'] = []  # TODO ListedJob.remote_listing()
    context['jobs_internship'] = []  # TODO ListedJob.internship_listing()
    context['jobs_volunteering'] = []  # TODO ListedJob.volunteering_listing()

    # open.md
    charts_months = charts.months(BUSINESS_BEGIN_ON, TODAY)
    context['charts_labels'] = charts.labels(charts_months)
    context['charts_revenue'] = charts.per_month(Transaction.revenue, charts_months)
    context['charts_revenue_ttm'] = charts.per_month(Transaction.revenue_ttm, charts_months)
    context['charts_revenue_breakdown'] = charts.per_month_breakdown(Transaction.revenue_breakdown, charts_months)
    context['charts_cost'] = charts.per_month(Transaction.cost, charts_months)
    context['charts_cost_ttm'] = charts.per_month(Transaction.cost_ttm, charts_months)
    context['charts_cost_breakdown'] = charts.per_month_breakdown(Transaction.cost_breakdown, charts_months)

    # podcast.md, handbook/cv.md
    context['podcast_episodes'] = PodcastEpisode.listing()


@db.connection_context()
def on_docs_page_context(context, page, config, files):
    if 'topic_name' in page.meta:
        topic_name = page.meta['topic_name']
        context['topic'] = Topic.get_by_id(topic_name)


####################################################################
# THEME CONTEXT                                                    #
####################################################################


def on_theme_context(context):
    js_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle.js'
    css_path = Path(__file__).parent.parent / 'web' / 'static' / 'bundle-mkdocs.css'
    context['js_hash'] = hash_file(js_path)
    context['css_hash'] = hash_file(css_path)
    context['bootstrap_icons_file'] = re.search(r'bootstrap-icons.woff2\?\w+', css_path.read_text()).group(0)

    context['companies_handbook'] = Company.handbook_listing()


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
