from datetime import UTC, datetime
from flask import Flask, render_template, url_for
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
    freezer = Freezer(app)
    freezer.register_generator(generate_job_pages)
    freezer.register_generator(generate_jobs_region_pages)
    return freezer


app = Flask(__name__)


def redirect(url):
    return render_template("meta_redirect.html", url=url)


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


@app.route("/jobs/region/<region_id>/")
@db.connection_context()
def jobs_region(region_id):
    region = [reg for reg in REGIONS if reg["id"] == region_id][0]
    jobs = ListedJob.region_listing(region["name"])
    jobs_remote = ListedJob.remote_listing()
    return render_template(
        "jobs_region.html",
        nav_active="jobs",
        jobs=jobs,
        jobs_remote=jobs_remote,
        region=region,
        regions=REGIONS,
        thumbnail=LegacyThumbnail.image_path_by_url(f"/jobs/region/{region_id}/"),
    )


def generate_jobs_region_pages():
    return [("jobs_region", dict(region_id=region["id"])) for region in REGIONS]


@app.route("/jobs/<job_id>/")
@db.connection_context()
def job(job_id):
    job = ListedJob.get_by_submitted_id(job_id)
    jobs_count = ListedJob.count()
    return render_template(
        "job.html",
        nav_active="jobs",
        job=job,
        jobs_count=jobs_count,
        thumbnail=LegacyThumbnail.image_path_by_url(f"/jobs/{job_id}/"),
    )


def generate_job_pages():
    with db.connection_context():
        jobs = list(ListedJob.submitted_listing())
    for job in jobs:
        yield "job", dict(job_id=job.submitted_job.id)


@app.route("/404.html")
@db.connection_context()
def not_found():
    jobs = ListedJob.listing()
    return render_template(
        "404.html", jobs=jobs, thumbnail=LegacyThumbnail.image_path_by_url("/404.html")
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


@app.route("/jobs/")
def jobs():
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
    return redirect(url_for("club", _external=True) + "#honza")


@app.route("/press/handbook/")
def press_release_handbook():
    return redirect(url_for("club", _external=True) + "#honza")


@app.route("/press/women/")
def press_release_women():
    return redirect(url_for("club", _external=True) + "#honza")


@app.route("/press/crisis/")
def press_release_crisis():
    return redirect(url_for("club", _external=True) + "#honza")
