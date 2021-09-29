from juniorguru.models.club import ClubUser
import os
from pathlib import Path

import arrow
from flask import Flask, Response, render_template, url_for

from juniorguru.lib.log import get_log
from juniorguru.lib import template_filters
from juniorguru.lib.images import render_image_file
from juniorguru.models import Job, Metric, Story, Supporter, LastModified, PressRelease, Logo, Company, Event, db


log = get_log('web')


FLUSH_THUMBNAILS = bool(int(os.getenv('FLUSH_THUMBNAILS', 0)))
THUMBNAILS_DIR = Path(__file__).parent / 'static' / 'images' / 'thumbnails'
THUMBNAIL_WIDTH = 1200
THUMBNAIL_HEIGHT = 630


NAV_TABS = [
    {'endpoint': 'motivation', 'name': 'Příručka'},
    {'endpoint': 'jobs', 'name': 'Práce'},
    {'endpoint': 'club', 'name': 'Klub'},
]

JOBS_SUBNAV_TABS = [
    {'endpoint': 'jobs', 'name': 'Nabídky práce'},
    {'endpoint': 'hire_juniors', 'name': 'Pro firmy'},
]

HANDBOOK_SUBNAV_TABS = [
    {'endpoint': 'motivation', 'name': 'Motivace', 'number': 0},
    {'endpoint': 'learn', 'name': 'Základy', 'number': 1},
    {'endpoint': 'practice', 'name': 'První praxe', 'number': 2},
    {'endpoint': 'candidate_handbook', 'name': 'Hledání práce', 'number': 3},
]

CLUB_SUBNAV_TABS = [
    {'endpoint': 'club', 'name': 'O klubu'},
    {'endpoint': 'events', 'name': 'Akce'},
    {'endpoint': 'membership', 'name': 'Pro členy'},
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
    log.warning("Removing all existing thumbnails, FLUSH_THUMBNAILS is set")
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
]:
    app.template_filter()(template_filter)


@app.route('/')
def index():
    with db:
        metrics = Job.aggregate_metrics()
        stories = Story.listing()
    return render_template('index.html',
                           nav_tabs=NAV_TABS,
                           metrics=metrics,
                           stories=stories)


@app.route('/club/')
def club():
    with db:
        members = ClubUser.avatars_listing()
        members_total_count = ClubUser.members_count()
        companies = Company.listing()
    return render_template('club.html',
                           nav_active='club',
                           subnav_tabs=CLUB_SUBNAV_TABS,
                           subnav_active='club',
                           companies=companies,
                           members=members,
                           members_total_count=members_total_count,
                           thumbnail=thumbnail(title='Klub, který tě nastartuje'))


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
                           subnav_tabs=CLUB_SUBNAV_TABS,
                           subnav_active='events',
                           events_planned=events_planned,
                           events_archive=events_archive,
                           thumbnail=thumbnail_path)


@app.route('/membership/')
def membership():
    return render_template('membership.html',
                           nav_active='club',
                           subnav_tabs=CLUB_SUBNAV_TABS,
                           subnav_active='membership',
                           thumbnail=thumbnail(title='Rozcestník pro členy klubu'))



@app.route('/motivation/')
def motivation():
    with db:
        stories = Story.listing()
        stories_by_tags = Story.tags_mapping()
    return render_template('motivation.html',
                           nav_active='motivation',
                           subnav_tabs=HANDBOOK_SUBNAV_TABS,
                           subnav_active='motivation',
                           stories=stories,
                           stories_by_tags=stories_by_tags,
                           thumbnail=thumbnail(title='Proč se učit programování'))


@app.route('/learn/')
def learn():
    with db:
        stories_count = len(Story.listing())
    return render_template('learn.html',
                           nav_active='motivation',
                           subnav_tabs=HANDBOOK_SUBNAV_TABS,
                           subnav_active='learn',
                           stories_count=stories_count,
                           thumbnail=thumbnail(title='Jak se naučit programovat'))


@app.route('/practice/')
def practice():
    return render_template('practice.html',
                           nav_active='motivation',
                           subnav_tabs=HANDBOOK_SUBNAV_TABS,
                           subnav_active='practice',
                           thumbnail=thumbnail(title='Jak získat praxi v\u00a0programování'))


@app.route('/candidate-handbook/')
def candidate_handbook():
    with db:
        jobs = Job.listing()
        jobs_remote = Job.remote_listing()
        jobs_internship = Job.internship_listing()
        jobs_volunteering = Job.volunteering_listing()
        supporters_count = Supporter.count()
        last_modified = LastModified.get_value_by_path('candidate_handbook.html')
        logos = Logo.listing()
    return render_template('candidate_handbook.html',
                           nav_active='motivation',
                           subnav_tabs=HANDBOOK_SUBNAV_TABS,
                           subnav_active='candidate_handbook',
                           jobs=jobs,
                           jobs_remote=jobs_remote,
                           jobs_internship=jobs_internship,
                           jobs_volunteering=jobs_volunteering,
                           supporters_count=supporters_count,
                           last_modified=last_modified,
                           logos=logos,
                           thumbnail=thumbnail(title='Příručka o\u00a0hledání první práce v\u00a0IT'))


@app.route('/jobs/')
def jobs():
    with db:
        metrics = dict(**Metric.as_dict(), **Job.aggregate_metrics())
        jobs = Job.listing()
    return render_template('jobs.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           regions=REGIONS,
                           metrics=metrics,
                           thumbnail=thumbnail(title='Práce v\u00a0IT pro začátečníky'))


@app.route('/jobs/remote/')
def jobs_remote():
    with db:
        metrics = dict(**Metric.as_dict(), **Job.aggregate_metrics())
        jobs = Job.remote_listing()
    return render_template('jobs_remote.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           remote=True,
                           regions=REGIONS,
                           metrics=metrics,
                           thumbnail=thumbnail(title='Práce v\u00a0IT pro začátečníky —\u00a0na\u00a0dálku'))


@app.route('/jobs/region/<region_id>/')
def jobs_region(region_id):
    region = [reg for reg in REGIONS if reg['id'] == region_id][0]
    with db:
        metrics = dict(**Metric.as_dict(), **Job.aggregate_metrics())
        jobs = Job.region_listing(region['name'])
        jobs_remote = Job.remote_listing()
    return render_template('jobs_region.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           jobs_remote=jobs_remote,
                           region=region,
                           regions=REGIONS,
                           metrics=metrics,
                           thumbnail=thumbnail(title=f"Práce v\u00a0IT pro začátečníky —\u00a0{region['name']}"))


@app.route('/jobs/<job_id>/')
def job(job_id):
    with db:
        metrics = dict(**Metric.as_dict(), **Job.aggregate_metrics())
        job = Job.juniorguru_get_by_id(job_id)
    return render_template('job.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           job=job,
                           metrics=metrics,
                           thumbnail=thumbnail(job_title=job.title,
                                               job_company=job.company_name,
                                               job_location=job.location))


def generate_job_pages():
    with db:
        for job in Job.juniorguru_listing():
            yield 'job', dict(job_id=job.id)


@app.route('/hire-juniors/')
def hire_juniors():
    with db:
        metrics = Metric.as_dict()
        members_total_count = ClubUser.members_count()
    return render_template('hire_juniors.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='hire_juniors',
                           metrics=metrics,
                           members_total_count=members_total_count,
                           thumbnail=thumbnail(title='Najímejte odhodlané juniory'))


@app.route('/donate/')
def donate():
    with db:
        supporters_names_urls = Supporter.listing_names_urls()
        supporters_names = Supporter.listing_names()
    return render_template('donate.html',
                           supporters_names_urls=supporters_names_urls,
                           supporters_names=supporters_names,
                           thumbnail=thumbnail(title='Pošli LOVE'))


@app.route('/press/')
def press():
    with db:
        press_releases = PressRelease.listing()
    return render_template('press.html',
                           press_releases=press_releases,
                           thumbnail=thumbnail(title='Pro média'))


@app.route('/press/<id>/')
def press_release(id):
    with db:
        press_release = PressRelease.get_by_id(id)
    return render_template('press_release.html',
                           press_release=press_release,
                           thumbnail=thumbnail(title='Tisková zpráva'))


@app.route('/404.html')
def not_found():
    with db:
        jobs = Job.listing()
    return render_template('404.html', jobs=jobs)


@app.route('/robots.txt')
def robots():
    return Response(f"User-agent: *\nDisallow: {url_for('admin')}\n",
                    mimetype='text/plain')


@app.route('/.nojekyll')
def nojekyll():
    return Response('', mimetype='application/octet-stream')


@app.route('/CNAME')
def cname():
    return Response('junior.guru\n', mimetype='application/octet-stream')


@app.context_processor
def inject_defaults():
    now = arrow.utcnow()
    return dict(nav_tabs=NAV_TABS,
                now=now,
                club_launch_at=arrow.get(2021, 2, 1),
                thumbnail=thumbnail())


from juniorguru.web import admin  # noqa
