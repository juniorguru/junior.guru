import os
from pathlib import Path

import arrow
from flask import Flask, render_template, url_for

from juniorguru.lib import loggers
from juniorguru.lib import template_filters
from juniorguru.lib.images import render_image_file
from juniorguru.models import ListedJob, Story, Supporter, Event, db


logger = loggers.get(__name__)


FLUSH_THUMBNAILS = bool(int(os.getenv('FLUSH_THUMBNAILS', 0)))
THUMBNAILS_DIR = Path(__file__).parent / 'static' / 'images' / 'thumbnails'
THUMBNAIL_WIDTH = 1200
THUMBNAIL_HEIGHT = 630


NAV_TABS = [
    {'endpoint': 'motivation', 'name': 'Příručka'},
    {'endpoint': 'jobs', 'name': 'Práce'},
    {'endpoint': 'club', 'name': 'Klub'},
]


REGIONS = [
    # tech hubs
    {'id': 'praha', 'name': 'Praha', 'name_in': 'v Praze', 'type': 'tech_hub'},
    {'id': 'brno', 'name': 'Brno', 'name_in': 'v Brně', 'type': 'tech_hub'},
    {'id': 'ostrava', 'name': 'Ostrava', 'name_in': 'v Ostravě', 'type': 'tech_hub'},

    # regions
    {'id': 'ceske-budejovice', 'name': 'České Budějovice', 'name_in': 'v Českých Budějovicích', 'type': 'region'},
    {'id': 'hradec-kralove', 'name': 'Hradec Králové', 'name_in': 'v Hradci Králové', 'type': 'region'},
    {'id': 'jihlava', 'name': 'Jihlava', 'name_in': 'v Jihlavě', 'type': 'region'},
    {'id': 'karlovy-vary', 'name': 'Karlovy Vary', 'name_in': 'v Karlových Varech', 'type': 'region'},
    {'id': 'liberec', 'name': 'Liberec', 'name_in': 'v Liberci', 'type': 'region'},
    {'id': 'olomouc', 'name': 'Olomouc', 'name_in': 'v Olomouci', 'type': 'region'},
    {'id': 'pardubice', 'name': 'Pardubice', 'name_in': 'v Pardubicích', 'type': 'region'},
    {'id': 'plzen', 'name': 'Plzeň', 'name_in': 'v Plzni', 'type': 'region'},
    {'id': 'usti-nad-labem', 'name': 'Ústí nad Labem', 'name_in': 'v Ústí nad Labem', 'type': 'region'},
    {'id': 'zlin', 'name': 'Zlín', 'name_in': 've Zlíně', 'type': 'region'},

    # countries
    {'id': 'germany', 'name': 'Německo', 'name_in': 'v Německu', 'type': 'country'},
    {'id': 'poland', 'name': 'Polsko', 'name_in': 'v Polsku', 'type': 'country'},
    {'id': 'austria', 'name': 'Rakousko', 'name_in': 'v Rakousku', 'type': 'country'},
    {'id': 'slovakia', 'name': 'Slovensko', 'name_in': 'na Slovensku', 'type': 'country'},
]


app = Flask(__name__)


if FLUSH_THUMBNAILS:
    logger.warning("Removing all existing thumbnails, FLUSH_THUMBNAILS is set")
    for thumbnail_path in THUMBNAILS_DIR.glob('*.png'):
        thumbnail_path.unlink()


def redirect(url):
    return render_template('meta_redirect.html', url=url)


def thumbnail(**context):
    image_path = render_image_file(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT,
                                   'thumbnail_legacy.html', context, THUMBNAILS_DIR)
    return f'images/thumbnails/{image_path.name}'


for template_filter in [
    template_filters.email_link,
    template_filters.md,
    template_filters.remove_p,
    template_filters.tag_label,
    template_filters.to_datetime,
    template_filters.ago,
    template_filters.sections,
    template_filters.metric,
    template_filters.sample,
    template_filters.sample_jobs,
    template_filters.local_time,
    template_filters.relative_url,
]:
    app.template_filter()(template_filter)


@app.route('/')
def index():
    with db:
        stories = Story.listing()
    return render_template('index.html',
                           nav_tabs=NAV_TABS,
                           stories=stories)


@app.route('/events/')
def events():
    with db:
        event_next = Event.next()
        events_planned = Event.planned_listing()
        events_archive = Event.archive_listing()
    if event_next:
        thumbnail_path = f'images/{event_next.poster_path}'
    else:
        thumbnail_path = thumbnail(title='Klubové akce')
    return render_template('events.html',
                           nav_active='club',
                           events_planned=events_planned,
                           events_archive=events_archive,
                           thumbnail=thumbnail_path)


@app.route('/membership/')
def membership():
    return render_template('membership.html',
                           nav_active='club',
                           thumbnail=thumbnail(title='Rozcestník pro členy klubu'))


@app.route('/jobs/')
@db.connection_context()
def jobs():
    jobs = ListedJob.listing()
    return render_template('jobs.html',
                           nav_active='jobs',
                           jobs=jobs,
                           regions=REGIONS,
                           thumbnail=thumbnail(title='Práce v IT pro začátečníky'))


@app.route('/jobs/remote/')
@db.connection_context()
def jobs_remote():
    jobs = ListedJob.remote_listing()
    return render_template('jobs_remote.html',
                           nav_active='jobs',
                           jobs=jobs,
                           remote=True,
                           regions=REGIONS,
                           thumbnail=thumbnail(title='Práce v\u00a0IT pro začátečníky —\u00a0na\u00a0dálku'))


@app.route('/jobs/region/<region_id>/')
@db.connection_context()
def jobs_region(region_id):
    region = [reg for reg in REGIONS if reg['id'] == region_id][0]
    jobs = ListedJob.region_listing(region['name'])
    jobs_remote = ListedJob.remote_listing()
    return render_template('jobs_region.html',
                           nav_active='jobs',
                           jobs=jobs,
                           jobs_remote=jobs_remote,
                           region=region,
                           regions=REGIONS,
                           thumbnail=thumbnail(title=f"Práce v\u00a0IT pro začátečníky —\u00a0{region['name']}"))


def generate_jobs_region_pages():
    return [('jobs_region', dict(region_id=region['id'])) for region in REGIONS]


@app.route('/jobs/<job_id>/')
@db.connection_context()
def job(job_id):
    job = ListedJob.get_by_submitted_id(job_id)
    jobs_count = ListedJob.count()
    return render_template('job.html',
                           nav_active='jobs',
                           job=job,
                           jobs_count=jobs_count,
                           thumbnail=thumbnail(job_title=job.title,
                                               job_company=job.company_name,
                                               job_location=job.location))


def generate_job_pages():
    with db.connection_context():
        jobs = list(ListedJob.submitted_listing())
    for job in jobs:
        yield 'job', dict(job_id=job.submitted_job.id)


@app.route('/donate/')
def donate():
    with db:
        supporters_names_urls = Supporter.listing_names_urls()
        supporters_names = Supporter.listing_names()
    return render_template('donate.html',
                           supporters_names_urls=supporters_names_urls,
                           supporters_names=supporters_names,
                           thumbnail=thumbnail(title='Pošli LOVE'))


@app.route('/handbook/')
def handbook():
    return redirect(url_for('motivation', _external=True))


@app.route('/404.html')
@db.connection_context()
def not_found():
    jobs = ListedJob.listing()
    return render_template('404.html', jobs=jobs)


@app.context_processor
def inject_defaults():
    now = arrow.utcnow()
    return dict(nav_tabs=NAV_TABS,
                now=now,
                club_launch_at=arrow.get(2021, 2, 1),
                thumbnail=thumbnail())


# Pages moved to MkDocs
#
# These pages have been moved to MkDocs. Keeping them here so that 'url_for()' works throughout
# the original code. Also fixing local reload when developing. Flask first generates this
# empty page with refresh, and it's in the browser until MkDocs are ready. The refresh avoids
# the annoying need for manual refresh.

REFRESH_PAGE = '<html><head><meta http-equiv="refresh" content="5"></head><body></body></html>'

@app.route('/club/')
def club():
    return REFRESH_PAGE

@app.route('/motivation/')
def motivation():
    return REFRESH_PAGE

@app.route('/learn/')
def learn():
    return REFRESH_PAGE

@app.route('/practice/')
def practice():
    return REFRESH_PAGE

@app.route('/candidate-handbook/')
def candidate_handbook():
    return REFRESH_PAGE

@app.route('/hire-juniors/')
def hire_juniors():
    return redirect(url_for('jobs', _external=True))

@app.route('/press/')
def press():
    return redirect(url_for('club', _external=True) + '#honza')

@app.route('/press/handbook/')
def press_release_handbook():
    return redirect(url_for('club', _external=True) + '#honza')

@app.route('/press/women/')
def press_release_women():
    return redirect(url_for('club', _external=True) + '#honza')

@app.route('/press/crisis/')
def press_release_crisis():
    return redirect(url_for('club', _external=True) + '#honza')
