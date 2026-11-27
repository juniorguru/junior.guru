from datetime import UTC, date, datetime, timedelta

from markupsafe import Markup

from jg.coop.lib import brand, loggers, months
from jg.coop.lib.discord_club import (
    CLUB_EVENTS_CHANNEL_URL,
    CLUB_GUILD_ID,
    CLUB_JOBS_CHANNEL_URL,
    ClubChannelID,
    ClubMemberID,
)
from jg.coop.lib.donations import (
    DONATION_AMOUNT_CZK,
    DONATION_MESSAGE,
    coverage_ptc,
    qr_payment_svg,
)
from jg.coop.models.base import db
from jg.coop.models.blog import BlogArticle
from jg.coop.models.candidate import Candidate
from jg.coop.models.chart import Chart
from jg.coop.models.club import ClubChannel, ClubMessage, ClubUser
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.exchange_rate import ExchangeRate
from jg.coop.models.external_story import ExternalStory
from jg.coop.models.followers import Followers
from jg.coop.models.job import (
    REMOTE_TAG_SLUG,
    DiscordJob,
    ListedJob,
    TagType,
)
from jg.coop.models.jobs_listing import (
    JOBS_CLUB_POSITION,
    JOBS_FORM_POSITION,
    JobsListingPage,
    get_jobs_filters,
    get_jobs_slots,
    get_listings_nav,
    get_location_tags,
)
from jg.coop.models.newsletter import NewsletterIssue
from jg.coop.models.page import Page
from jg.coop.models.partner import Partner
from jg.coop.models.podcast import PodcastEpisode
from jg.coop.models.role import InterestRole
from jg.coop.models.sponsor import GitHubSponsor, PastSponsor, Sponsor
from jg.coop.models.stage import Stage
from jg.coop.models.topic import TopicDiscussion, TopicMention
from jg.coop.models.transaction import Transaction, TransactionsCategory
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
    context["club_events_channel_url"] = CLUB_EVENTS_CHANNEL_URL

    # main.html, index.jinja, about/*.md, love.jinja
    context["sponsors_github"] = GitHubSponsor.listing()

    # main.html, about/*.md
    profit_ttm = Transaction.profit_ttm(today)
    context["profit_ttm"] = profit_ttm
    context["revenue_ttm_breakdown"] = Transaction.revenue_ttm_breakdown(today)

    # about/*.md
    context["profit_ttm_usd"] = ExchangeRate.in_currency(profit_ttm, "USD")
    context["profit_ttm_eur"] = ExchangeRate.in_currency(profit_ttm, "EUR")

    # club.md, courses/*.md, main_content_detail.html, love.jinja
    context["members"] = ClubUser.avatars_listing()

    # club.md, about/*.md, main_content_detail.html, love.jinja
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
    # index.jinja
    context["handbook_pages_count"] = Page.handbook_count()
    context["jobs_listed_count"] = ListedJob.count()
    context["candidates_promo"] = list(Candidate.promo_listing())
    context["candidates_count"] = Candidate.count()

    # club.md, about/*.md
    context["sponsors_by_tier"] = Sponsor.tier_grouping()

    # club.md, handbook/cv.md, handbook/mental-health.md
    context["events"] = Event.listing()
    context["events_recordings_count"] = len(Event.archive_listing(has_recording=True))
    club_diaries_threads = list(
        ClubMessage.forum_top_listing(
            ClubChannelID.DIARIES, months.prev_month(datetime.now(UTC).date())
        )
    )
    club_diaries = [
        {
            "name": message.channel_name,
            "url": message.url,
            "author": ClubChannel.get_by_id(message.channel_id).author.display_name,
        }
        for message in club_diaries_threads
        if ClubChannel.get_by_id(message.channel_id).author.id != ClubMemberID.HONZA
    ]
    context["club_diaries"] = club_diaries

    # club.md
    context["messages_count"] = ClubMessage.count()
    context["events_promo"] = Event.promo_listing()
    context["interests"] = InterestRole.interests()
    context["topic_discussions"] = TopicDiscussion.listing()

    # club.md, about/*.md
    context["sponsors"] = Sponsor.listing()
    context["partners"] = Partner.listing()

    # love.jinja
    context.update(get_love_context(date.today()))

    # courses.md
    context["course_providers_by_group"] = CourseProvider.grouping()

    # candidates.jinja
    context.update(get_candidates_context())

    # handbook/index.md
    context["stages"] = Stage.listing()

    # handbook/motivation.md
    context["external_stories_by_tags"] = ExternalStory.tags_mapping()

    # jobs.jinja, handbook/candidate.md
    context.update(get_jobs_context())

    # about/*.md
    context["blog"] = BlogArticle.listing()
    context["sponsors_past"] = PastSponsor.listing()
    context["sponsors_github_past"] = GitHubSponsor.past_listing()
    context["handbook_total_size"] = Page.handbook_total_size()

    # about/*.md, love.jinja, club.md
    context["charts"] = Chart.as_dict()

    # podcast.md, handbook/cv.md, news.jinja
    context["podcast_episodes"] = PodcastEpisode.listing()

    # events.md, news.jinja
    context["events_planned"] = Event.planned_listing()
    context["events_archive"] = Event.archive_listing()

    # stories.md, news.jinja
    context["external_stories_links"] = ExternalStory.listing()
    context["stories_pages"] = Page.stories_listing()

    # wisdom.jinja, news.jinja
    context["wisdoms"] = Wisdom.listing()

    # news.jinja
    context["newsletter_subscribers_count"] = Followers.get_latest("newsletter").count
    context["newsletter_issues"] = NewsletterIssue.listing()
    context["club_guild_id"] = CLUB_GUILD_ID
    context["channels_digest"] = ClubMessage.digest_channels(
        date.today() - timedelta(days=7), limit=5
    )


def get_love_context(today: date) -> dict:
    return build_love_context(
        Transaction.revenue_ttm_breakdown(today),
        Transaction.cost_ttm(today),
        github_sponsors_czk=ExchangeRate.from_currency(4, "USD"),
    )


def build_love_context(
    revenue_breakdown: dict[str, int], cost: int, github_sponsors_czk: int
) -> dict:
    return {
        "github_sponsors_czk": github_sponsors_czk,
        "donation_amount_czk": DONATION_AMOUNT_CZK,
        "donation_qr_svg": Markup(
            qr_payment_svg(
                brand.BANK_ACCOUNT,
                brand.BANK_BIC,
                DONATION_AMOUNT_CZK,
                brand.DONATIONS_VARIABLE_SYMBOL,
                DONATION_MESSAGE,
            )
        ),
        "donations_coverage_ptc": coverage_ptc(
            revenue_breakdown, cost, TransactionsCategory.DONATIONS
        ),
    }


def get_jobs_context() -> dict:
    listings = list(JobsListingPage.listing())
    location_tags = get_location_tags(listings)
    jobs = list(ListedJob.listing())
    # Manual jobs from Discord show on every listing page, whatever its tags
    jobs_discord = list(DiscordJob.listing())
    jobs_by_listing = {listing.slug: list(listing.list_jobs()) for listing in listings}
    return {
        "jobs": jobs,
        "jobs_slots": get_jobs_slots(jobs, jobs_discord),
        "jobs_discord": jobs_discord,
        "jobs_remote": ListedJob.tagged_listing(TagType.LOCATION, [REMOTE_TAG_SLUG]),
        "jobs_internship": ListedJob.tagged_listing(TagType.EMPLOYMENT, ["internship"]),
        "jobs_volunteering": ListedJob.tagged_listing(
            TagType.EMPLOYMENT, ["volunteering"]
        ),
        "jobs_filters": get_jobs_filters(ListedJob.tags_by_type(), location_tags),
        "jobs_listings": {listing.slug: listing for listing in listings},
        "jobs_by_listing": jobs_by_listing,
        "jobs_slots_by_listing": {
            slug: get_jobs_slots(listing_jobs, jobs_discord)
            for slug, listing_jobs in jobs_by_listing.items()
        },
        "jobs_filters_by_listing": {
            listing.slug: get_jobs_filters(
                ListedJob.tags_by_type(listing.list_jobs()), location_tags, listing
            )
            for listing in listings
        },
        "jobs_remote_tag_slug": REMOTE_TAG_SLUG,
        "jobs_club_position": JOBS_CLUB_POSITION,
        "jobs_form_position": JOBS_FORM_POSITION,
        "club_jobs_channel_url": CLUB_JOBS_CHANNEL_URL,
    }


def get_candidates_context() -> dict:
    return {
        "candidates": Candidate.listing(),
        "candidates_tags": Candidate.tags_by_type(),
        "candidates_region_tags": Candidate.region_tags(),
    }


@db.connection_context()
def on_docs_page_context(context, page, config, files):
    meta_model_getters = (
        ("course_provider_slug", CourseProvider.get_by_slug, "course_provider"),
        ("event_id", Event.get_by_id, "event"),
        ("job_id", ListedJob.get_by_submitted_id, "job"),
        ("jobs_listing_slug", JobsListingPage.get_by_slug, "jobs_listing"),
        ("newsletter_issue_id", NewsletterIssue.get_by_id, "newsletter_issue"),
        ("podcast_episode_number", PodcastEpisode.get_by_number, "podcast_episode"),
        ("topic_mention_id", TopicMention.get_by_id, "topic_mention"),
    )
    for meta_key, model_getter, model_var in meta_model_getters:
        if meta_key in page.meta:
            context[model_var] = model_getter(page.meta[meta_key])


####################################################################
# THEME CONTEXT                                                    #
####################################################################


@db.connection_context()
def on_theme_context(context):
    context["promo_stories"] = Page.stories_listing()
    context["promo_events"] = Event.featured_listing()
    context["newsletter_subscribers_count"] = Followers.get_latest("newsletter").count
    context["sponsors"] = Sponsor.listing()

    # main_jobs.html
    context["jobs_listing_pages"] = list(JobsListingPage.listing())


@db.connection_context()
def on_theme_page_context(context, page, config, files):
    # main_jobs.html
    context["jobs_listings_nav"] = get_listings_nav(
        context["jobs_listing_pages"], page.file.src_uri
    )

    try:
        current_page = Page.get_by_src_uri(page.file.src_uri)
    except Page.DoesNotExist:
        logger.debug(f"No data for {page.file.src_uri}, probably redirect")
    else:
        if thumbnail_url := current_page.thumbnail_url:
            context["thumbnail_url"] = thumbnail_url
        else:
            logger.warning(f"No thumbnail for {page.file.src_uri}")
        context["related_pages"] = current_page.list_related()
        context["related_channels"] = current_page.list_related_channels()
        context["related_channels_monthly_size"] = (
            current_page.related_channels_monthly_size
        )
