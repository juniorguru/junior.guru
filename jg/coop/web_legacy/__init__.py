from datetime import UTC, datetime

from flask import Flask, render_template
from flask_frozen import Freezer

from jg.coop.lib import loggers, template_filters
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob
from jg.coop.models.page import LegacyThumbnail


logger = loggers.from_path(__file__)


NAV_TABS = [
    {"endpoint": "club", "name": "Klub"},
    {"endpoint": "handbook", "name": "Příručka"},
    {"endpoint": "courses", "name": "Kurzy"},
    {"endpoint": "jobs", "name": "Práce"},
    {"endpoint": "news", "name": "Inspirace"},
]


REGIONS = [
    # tech hubs
    {"id": "praha", "name": "Praha", "name_in": "v Praze", "type": "tech_hub"},
    {"id": "brno", "name": "Brno", "name_in": "v Brně", "type": "tech_hub"},
    {"id": "ostrava", "name": "Ostrava", "name_in": "v Ostravě", "type": "tech_hub"},
    # regions
    {
        "id": "ceske-budejovice",
        "name": "České Budějovice",
        "name_in": "v Českých Budějovicích",
        "type": "region",
    },
    {
        "id": "hradec-kralove",
        "name": "Hradec Králové",
        "name_in": "v Hradci Králové",
        "type": "region",
    },
    {"id": "jihlava", "name": "Jihlava", "name_in": "v Jihlavě", "type": "region"},
    {
        "id": "karlovy-vary",
        "name": "Karlovy Vary",
        "name_in": "v Karlových Varech",
        "type": "region",
    },
    {"id": "liberec", "name": "Liberec", "name_in": "v Liberci", "type": "region"},
    {"id": "olomouc", "name": "Olomouc", "name_in": "v Olomouci", "type": "region"},
    {
        "id": "pardubice",
        "name": "Pardubice",
        "name_in": "v Pardubicích",
        "type": "region",
    },
    {"id": "plzen", "name": "Plzeň", "name_in": "v Plzni", "type": "region"},
    {
        "id": "usti-nad-labem",
        "name": "Ústí nad Labem",
        "name_in": "v Ústí nad Labem",
        "type": "region",
    },
    {"id": "zlin", "name": "Zlín", "name_in": "ve Zlíně", "type": "region"},
    # countries
    {"id": "germany", "name": "Německo", "name_in": "v Německu", "type": "country"},
    {"id": "poland", "name": "Polsko", "name_in": "v Polsku", "type": "country"},
    {"id": "austria", "name": "Rakousko", "name_in": "v Rakousku", "type": "country"},
    {
        "id": "slovakia",
        "name": "Slovensko",
        "name_in": "na Slovensku",
        "type": "country",
    },
]


def get_freezer(app) -> Freezer:
    return Freezer(app)


app = Flask(__name__)


for template_filter in [
    template_filters.email_link,
    template_filters.md,
    template_filters.remove_p,
    template_filters.sample,
    template_filters.sample_jobs,
    template_filters.relative_url,
]:
    app.template_filter()(template_filter)


@app.route("/jobs/remote/")
@db.connection_context()
def jobs_remote():
    jobs = ListedJob.remote_listing()
    return render_template(
        "jobs_remote.html",
        nav_active="jobs",
        jobs=jobs,
        remote=True,
        regions=REGIONS,
        thumbnail=LegacyThumbnail.image_path_by_url("/jobs/remote/"),
    )


@app.context_processor
def inject_defaults():
    now = datetime.now(UTC)
    return dict(nav_tabs=NAV_TABS, now=now, today=now.date())


# Pages moved to MkDocs
#
# These pages have been moved to MkDocs. Keeping them here so that 'url_for()' works throughout
# the original code. Also fixing local reload when developing. Flask first generates this
# empty page with refresh, and it's in the browser until MkDocs are ready. The refresh avoids
# the annoying need for manual refresh.

REFRESH_PAGE = (
    '<html><head><meta http-equiv="refresh" content="5"></head><body></body></html>'
)


@app.route("/")
def index():
    return REFRESH_PAGE


@app.route("/404.html")
def not_found():
    return REFRESH_PAGE


@app.route("/jobs/")
def jobs():
    return REFRESH_PAGE


@app.route("/jobs/<job_id>/")
def job(job_id):
    return REFRESH_PAGE


@app.route("/jobs/region/<region_id>/")
def jobs_region(region_id):
    return REFRESH_PAGE


@app.route("/news/")
def news():
    return REFRESH_PAGE


@app.route("/courses/")
def courses():
    return REFRESH_PAGE


@app.route("/events/")
def events():
    return REFRESH_PAGE


@app.route("/club/")
def club():
    return REFRESH_PAGE


@app.route("/podcast/")
def podcast():
    return REFRESH_PAGE


@app.route("/handbook/")
def handbook():
    return REFRESH_PAGE


@app.route("/handbook/candidate/")
def handbook_candidate():
    return REFRESH_PAGE


@app.route("/press/")
def press():
    return REFRESH_PAGE


@app.route("/press/handbook/")
def press_release_handbook():
    return REFRESH_PAGE


@app.route("/press/women/")
def press_release_women():
    return REFRESH_PAGE


@app.route("/press/crisis/")
def press_release_crisis():
    return REFRESH_PAGE
