from datetime import UTC, date, datetime, timedelta
from operator import attrgetter
from urllib.parse import urljoin

from jg.coop.lib import loggers
from jg.coop.lib.discord_club import CLUB_GUILD_ID
from jg.coop.models.base import db
from jg.coop.models.blog import BlogArticle
from jg.coop.models.candidate import Candidate
from jg.coop.models.chart import Chart
from jg.coop.models.club import ClubMessage, ClubUser
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.exchange_rate import ExchangeRate
from jg.coop.models.followers import Followers
from jg.coop.models.job import DiscordJob, ListedJob
from jg.coop.models.newsletter import NewsletterIssue
from jg.coop.models.page import Page
from jg.coop.models.partner import Partner
from jg.coop.models.podcast import PodcastEpisode
from jg.coop.models.role import InterestRole
from jg.coop.models.sponsor import GitHubSponsor, PastSponsor, Sponsor, SponsorTier
from jg.coop.models.stage import Stage
from jg.coop.models.story import Story
from jg.coop.models.topic import Topic
from jg.coop.models.transaction import Transaction
from jg.coop.models.wisdom import Wisdom


logger = loggers.from_path(__file__)


####################################################################
# SHARED DOCS AND THEME CONTEXT                                    #
####################################################################


@db.connection_context()
def on_shared_context(context):
    now = datetime.now(UTC)
    today = now.date()
    context["now"] = now
    context["today"] = today

    # main.html, about/*.md
    profit_ttm = Transaction.profit_ttm(today)
    context["profit_ttm"] = profit_ttm
    context["revenue_ttm_breakdown"] = Transaction.revenue_ttm_breakdown(today)

    # about/*.md
    context["profit_ttm_usd"] = ExchangeRate.in_currency(profit_ttm, "USD")
    context["profit_ttm_eur"] = ExchangeRate.in_currency(profit_ttm, "EUR")

    # club.md, courses/*.md, main_stories.html, love.jinja
    context["members"] = ClubUser.avatars_listing()

    # club.md, about/*.md, main_stories.html, love.jinja
    context["members_total_count"] = ClubUser.members_count()

    # about/handbook.md, main_handbook.html
    context["sponsors_handbook"] = Sponsor.handbook_listing()


def on_shared_page_context(context, page, config, files):
    pass


####################################################################
# DOCS CONTEXT                                                     #
####################################################################


@db.connection_context()
def on_docs_context(context):
    # index.jinja, about/*.md, love.jinja
    context["sponsors_github"] = GitHubSponsor.listing()

    # index.jinja, club.md, about/*.md
    context["sponsors_by_tier"] = Sponsor.tier_grouping()

    # club.md, handbook/cv.md, handbook/mental-health.md
    context["events"] = Event.listing()

    # club.md
    context["messages_count"] = ClubMessage.count()
    context["events_promo"] = Event.promo_listing()
    context["interests"] = InterestRole.interests()

    # club.md, about/*.md
    context["sponsors"] = Sponsor.listing()
    context["partners"] = Partner.listing()

    # love.jinja
    context["github_sponsors_czk"] = ExchangeRate.from_currency(4, "USD")
    context["sponsor_tiers"] = SponsorTier.pricing_listing()

    # courses.md
    context["course_providers_by_group"] = CourseProvider.grouping()

    # candidates.md
    context["candidates"] = Candidate.listing()

    # handbook/index.md
    context["stages"] = Stage.listing()

    # handbook/motivation.md
    context["stories_by_tags"] = Story.tags_mapping()

    # jobs.jinja, handbook/candidate.md
    context["jobs"] = ListedJob.listing()
    context["jobs_discord"] = DiscordJob.listing()
    context["jobs_remote"] = ListedJob.remote_listing()
    context["jobs_internship"] = ListedJob.internship_listing()
    context["jobs_volunteering"] = ListedJob.volunteering_listing()
    context["jobs_tags"] = ListedJob.tags_by_type()
    context["jobs_region_tags"] = ListedJob.region_tags()

    # about/*.md
    context["blog"] = BlogArticle.listing()
    context["sponsors_past"] = PastSponsor.listing()
    context["sponsors_github_past"] = GitHubSponsor.past_listing()
    context["handbook_total_size"] = Page.handbook_total_size()

    # about/*.md, love.jinja, club.md
    context["charts"] = Chart.as_dict()

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
    context["newsletter_issues"] = NewsletterIssue.listing()
    context["club_guild_id"] = CLUB_GUILD_ID
    context["channels_digest"] = ClubMessage.digest_channels(
        date.today() - timedelta(days=7), limit=5
    )


@db.connection_context()
def on_docs_page_context(context, page, config, files):
    meta_model_getters = (
        ("course_provider_slug", CourseProvider.get_by_slug, "course_provider"),
        ("event_id", Event.get_by_id, "event"),
        ("job_id", ListedJob.get_by_submitted_id, "job"),
        ("newsletter_issue_id", NewsletterIssue.get_by_id, "newsletter_issue"),
        ("podcast_episode_number", PodcastEpisode.get_by_number, "podcast_episode"),
        ("topic_name", Topic.get_by_id, "topic"),
    )
    for meta_key, model_getter, model_var in meta_model_getters:
        if meta_key in page.meta:
            context[model_var] = model_getter(page.meta[meta_key])


####################################################################
# THEME CONTEXT                                                    #
####################################################################


@db.connection_context()
def on_theme_context(context):
    context["course_providers"] = CourseProvider.listing()


@db.connection_context()
def on_theme_page_context(context, page, config, files):
    try:
        thumbnail_path = Page.get_by_src_uri(page.file.src_uri).thumbnail_path
    except Page.DoesNotExist:
        logger.debug(f"No thumbnail for {page.file.src_uri}, probably redirect")
    else:
        if thumbnail_path:
            context["thumbnail_url"] = urljoin(
                config["site_url"], f"static/{thumbnail_path}"
            )
        else:
            logger.warning(f"No thumbnail for {page.file.src_uri}")
