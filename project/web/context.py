import os
from datetime import date, timedelta
from operator import attrgetter
from urllib.parse import urljoin

import arrow

from project.lib import loggers
from project.lib.benefits_evaluators import BENEFITS_EVALUATORS
from project.lib.discord_club import CLUB_GUILD
from project.models.base import db
from project.models.blog import BlogArticle
from project.models.chart import Chart
from project.models.club import ClubMessage, ClubUser
from project.models.course_provider import CourseProvider
from project.models.event import Event
from project.models.exchange_rate import ExchangeRate
from project.models.followers import Followers
from project.models.job import ListedJob
from project.models.page import Page
from project.models.partner import Partner, Partnership
from project.models.podcast import PodcastEpisode
from project.models.stage import Stage
from project.models.story import Story
from project.models.topic import Topic
from project.models.transaction import Transaction
from project.models.wisdom import Wisdom


CLOUDINARY_HOST = os.getenv("CLOUDINARY_HOST", "res.cloudinary.com")


logger = loggers.from_path(__file__)


####################################################################
# SHARED DOCS AND THEME CONTEXT                                    #
####################################################################


@db.connection_context()
def on_shared_context(context):
    now = arrow.utcnow()
    today = now.date()
    context["now"] = now
    context["today"] = today

    # theme, but also macros.html used in .jinja pages
    context["cloudinary_host"] = CLOUDINARY_HOST

    # main.html
    context["revenue_ttm_breakdown"] = Transaction.revenue_ttm_breakdown(today)

    # main.html, open.md
    profit_ttm = Transaction.profit_ttm(today)
    context["profit_ttm"] = profit_ttm

    # open.md
    context["profit_ttm_usd"] = ExchangeRate.in_currency(profit_ttm, "USD")
    context["profit_ttm_eur"] = ExchangeRate.in_currency(profit_ttm, "EUR")

    # club.md, courses/*.md, main_stories.html
    context["members"] = ClubUser.avatars_listing()

    # club.md, open.md, main_stories.html
    context["members_total_count"] = ClubUser.members_count()


def on_shared_page_context(context, page, config, files):
    pass


####################################################################
# DOCS CONTEXT                                                     #
####################################################################


@db.connection_context()
def on_docs_context(context):
    # club.md
    context["messages_count"] = ClubMessage.count()
    context["events"] = Event.listing()
    context["events_promo"] = Event.promo_listing()

    # club.md, open.md
    context["partnerships"] = Partnership.active_listing()

    # courses.md
    context["course_providers"] = CourseProvider.listing()

    # faq.md
    context["partners_course_providers"] = [
        partner for partner in Partner.active_listing() if partner.course_provider
    ]

    # handbook/index.md
    context["stages"] = Stage.listing()

    # handbook/motivation.md
    context["stories_by_tags"] = Story.tags_mapping()

    # handbook/candidate.md
    context["jobs"] = ListedJob.listing()
    context["jobs_remote"] = ListedJob.remote_listing()
    context["jobs_internship"] = ListedJob.internship_listing()
    context["jobs_volunteering"] = ListedJob.volunteering_listing()

    # open.md
    context["blog"] = BlogArticle.listing()
    context["partners_expired"] = Partner.expired_listing()
    context["handbook_total_size"] = Page.handbook_total_size()
    context["charts"] = Chart.as_dict()

    # open/*
    context["benefits_evaluators"] = BENEFITS_EVALUATORS

    # index.jinja, podcast.md, handbook/cv.md, news.jinja
    context["podcast_episodes"] = PodcastEpisode.listing()

    # index.jinja, events.md, news.jinja
    context["events_planned"] = Event.planned_listing()
    context["events_archive"] = Event.archive_listing()

    # index.jinja, stories.md, news.jinja
    stories_links = list(Story.listing())
    stories_pages = list(Page.stories_listing())
    context["stories_links"] = stories_links
    context["stories_pages"] = stories_pages
    context["stories"] = sorted(
        stories_links + stories_pages, key=attrgetter("date"), reverse=True
    )

    # wisdom.jinja, news.jinja
    context["wisdoms"] = Wisdom.listing()

    # news.jinja
    context["newsletter_subscribers_count"] = Followers.get_latest("newsletter").count
    context["club_guild_id"] = CLUB_GUILD
    context["channels_digest"] = ClubMessage.digest_channels(
        date.today() - timedelta(days=7), limit=5
    )


@db.connection_context()
def on_docs_page_context(context, page, config, files):
    meta_model_getters = (
        ("topic_name", Topic.get_by_id, "topic"),
        ("event_id", Event.get_by_id, "event"),
        ("partner_slug", Partner.get_by_slug, "partner"),
        ("course_provider_slug", CourseProvider.get_by_slug, "course_provider"),
        ("podcast_episode_number", PodcastEpisode.get_by_number, "podcast_episode"),
    )
    for meta_key, model_getter, model_var in meta_model_getters:
        if meta_key in page.meta:
            context[model_var] = model_getter(page.meta[meta_key])


####################################################################
# THEME CONTEXT                                                    #
####################################################################


@db.connection_context()
def on_theme_context(context):
    context["partnerships_handbook"] = Partnership.handbook_listing()
    context["course_providers"] = CourseProvider.listing()


@db.connection_context()
def on_theme_page_context(context, page, config, files):
    try:
        thumbnail_path = Page.get_by_src_uri(page.file.src_uri).thumbnail_path
        context["thumbnail_url"] = urljoin(
            config["site_url"], f"static/{thumbnail_path}"
        )
    except Page.DoesNotExist:
        logger.warning(f"No thumbnail for {page.file.src_uri}")
