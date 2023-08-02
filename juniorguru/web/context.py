import os
from urllib.parse import urljoin

import arrow

from juniorguru.lib.benefits_evaluators import BENEFITS_EVALUATORS
from juniorguru.models.base import db
from juniorguru.models.blog import BlogArticle
from juniorguru.models.chart import Chart
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.models.course_provider import CourseProvider
from juniorguru.models.event import Event
from juniorguru.models.exchange_rate import ExchangeRate
from juniorguru.models.job import ListedJob
from juniorguru.models.page import Page
from juniorguru.models.partner import Partner, Partnership
from juniorguru.models.podcast import PodcastEpisode
from juniorguru.models.story import Story
from juniorguru.models.topic import Topic
from juniorguru.models.transaction import Transaction


CLOUDINARY_HOST = os.getenv('CLOUDINARY_HOST', 'res.cloudinary.com')


####################################################################
# SHARED DOCS AND THEME CONTEXT                                    #
####################################################################


@db.connection_context()
def on_shared_context(context):
    now = arrow.utcnow()
    today = now.date()

    context['now'] = now
    context['today'] = today

    context['cloudinary_host'] = CLOUDINARY_HOST

    profit_ttm = Transaction.profit_ttm(today)
    context['profit_ttm'] = profit_ttm
    context['profit_ttm_usd'] = ExchangeRate.in_currency(profit_ttm, 'USD')
    context['profit_ttm_eur'] = ExchangeRate.in_currency(profit_ttm, 'EUR')
    context['revenue_ttm_breakdown'] = Transaction.revenue_ttm_breakdown(today)


def on_shared_page_context(context, page, config, files):
    pass


####################################################################
# DOCS CONTEXT                                                     #
####################################################################


@db.connection_context()
def on_docs_context(context):
    # club.md, open.md
    context['members_total_count'] = ClubUser.members_count()

    # club.md
    context['messages_count'] = ClubMessage.count()
    context['partners_having_students'] = [partner for partner in Partner.active_listing() if partner.has_students]
    context['events'] = Event.listing()
    context['events_club'] = Event.club_listing()

    # club.md, open.md
    context['partnerships'] = Partnership.active_listing()

    # club.md, courses/*.md
    context['members'] = ClubUser.avatars_listing()

    # courses.md
    context['course_providers'] = CourseProvider.listing()

    # faq.md
    context['partners_course_providers'] = [partner for partner in Partner.active_listing() if partner.course_provider]

    # handbook/motivation.md
    context['stories'] = Story.listing()
    context['stories_by_tags'] = Story.tags_mapping()

    # handbook/candidate.md
    context['jobs'] = ListedJob.listing()
    context['jobs_remote'] = ListedJob.remote_listing()
    context['jobs_internship'] = ListedJob.internship_listing()
    context['jobs_volunteering'] = ListedJob.volunteering_listing()

    # open.md
    context['blog'] = BlogArticle.listing()
    context['partners_expired'] = Partner.expired_listing()
    context['handbook_total_size'] = Page.handbook_total_size()
    context['charts'] = Chart.as_dict()

    # open/*
    context['benefits_evaluators'] = BENEFITS_EVALUATORS

    # podcast.md, handbook/cv.md
    context['podcast_episodes'] = PodcastEpisode.listing()


@db.connection_context()
def on_docs_page_context(context, page, config, files):
    meta_model_getters = (
        ('topic_name', Topic.get_by_id, 'topic'),
        ('partner_slug', Partner.get_by_slug, 'partner'),
        ('course_provider_slug', CourseProvider.get_by_slug, 'course_provider'),
    )
    for meta_key, model_getter, model_var in meta_model_getters:
        if meta_key in page.meta:
            context[model_var] = model_getter(page.meta[meta_key])


####################################################################
# THEME CONTEXT                                                    #
####################################################################


@db.connection_context()
def on_theme_context(context):
    context['partnerships_handbook'] = Partnership.handbook_listing()
    context['course_providers'] = CourseProvider.listing()


@db.connection_context()
def on_theme_page_context(context, page, config, files):
    thumbnail_path = Page.get_by_src_uri(page.file.src_uri).thumbnail_path
    context['thumbnail_url'] = urljoin(config['site_url'], f'static/{thumbnail_path}')

    context['parent_page'] = get_parent_page(page)
    context['previous_page'] = get_sibling_page(page, -1)
    context['next_page'] = get_sibling_page(page, +1)


####################################################################
# HELPER FUNCTIONS                                                 #
####################################################################


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
