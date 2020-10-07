import arrow
from flask import Flask, Response, abort, render_template, url_for

from juniorguru.models import Job, Metric, Story, Supporter, LastModified, PressRelease, Logo, db
from juniorguru.web.thumbnail import thumbnail


NAV_TABS = [
    {'endpoint': 'learn', 'name': 'Nauč se základy', 'name_short': 'Základy'},
    {'endpoint': 'practice', 'name': 'Získej praxi', 'name_short': 'Praxe'},
    {'endpoint': 'jobs', 'name': 'Najdi práci', 'name_short': 'Práce'},
]

JOBS_SUBNAV_TABS = [
    {'endpoint': 'jobs', 'name': 'Nabídky práce'},
    {'endpoint': 'candidate_handbook', 'name': 'Příručka o hledání práce'},
    {'endpoint': 'hire_juniors', 'name': 'Pro firmy'},
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


def redirect(url):
    return render_template('meta_redirect.html', url=url)


@app.route('/')
def index():
    with db:
        metrics = Job.aggregate_metrics()
    return render_template('index.html',
                           nav_tabs=None,
                           metrics=metrics,
                           stories=Story.listing())


@app.route('/learn/')
def learn():
    return render_template('learn.html',
                           nav_active='learn',
                           stories_count=len(Story.listing()),
                           thumbnail=thumbnail(title='Jak se naučit programovat'))


@app.route('/practice/')
def practice():
    return render_template('practice.html',
                           nav_active='practice',
                           thumbnail=thumbnail(title='Jak získat praxi v\u00a0programování'))


@app.route('/candidate-handbook/')
def candidate_handbook():
    with db:
        metrics = Job.aggregate_metrics()
        supporters_count = Supporter.count()
        last_modified = LastModified.get_value_by_path('candidate_handbook.html')
        logos = Logo.listing()
    return render_template('candidate_handbook.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='candidate_handbook',
                           metrics=metrics,
                           supporters_count=supporters_count,
                           last_modified=last_modified,
                           logos=logos,
                           thumbnail=thumbnail(title='Příručka o\u00a0hledání první práce v\u00a0IT'))


@app.route('/candidate/')
def candidate():
    return redirect(url_for('candidate_handbook', _external=True))


@app.route('/__supercalifragilisticexpialidocious__/')
def candidate_handbook_teaser():
    return redirect(url_for('candidate_handbook', _external=True))


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
    return render_template('jobs_region.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           region=region,
                           regions=REGIONS,
                           metrics=metrics,
                           thumbnail=thumbnail(title=f"Práce v\u00a0IT pro začátečníky —\u00a0{region['name']}"))


@app.route('/jobs/<job_id>/')
def job(job_id):
    with db:
        metrics = dict(**Metric.as_dict(), **Job.aggregate_metrics())
        job = Job.get_by_id(job_id) or abort(404)
    return render_template('job.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           job=job,
                           metrics=metrics,
                           thumbnail=thumbnail(job_title=job.title,
                                               job_company=job.company_name,
                                               job_location=job.location))


@app.route('/hire-juniors/')
def hire_juniors():
    with db:
        metrics = Metric.as_dict()
    return render_template('hire_juniors.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='hire_juniors',
                           metrics=metrics,
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


@app.route('/thanks/')
def thanks():
    return render_template('thanks.html',
                           thumbnail=thumbnail(title='Díky!'))


@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')


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
#@app.route('/jobs/404.html')  # debug
def not_found():
    return render_template('404.html')


@app.route('/robots.txt')
def robots():
    return Response(f"User-agent: *\nDisallow: {url_for('admin')}\n",
                    mimetype='text/plain')


@app.context_processor
def inject_defaults():
    now = arrow.utcnow()
    return dict(nav_tabs=NAV_TABS,
                year=now.year,
                now=now,
                handbook_release_at=arrow.get(2020, 9, 1),
                thumbnail=thumbnail())


from juniorguru.web import admin, template_filters  # noqa
