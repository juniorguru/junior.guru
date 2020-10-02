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

REGIONS = {
    # Prague
    'praha': ('Praha', 'Praze'),

    # alphabetically
    'brno': ('Brno', 'v Brně'),
    'ceske-budejovice': ('České Budějovice', 'v Českých Budějovicích'),
    'hradec-kralove': ('Hradec Králové', 'v Hradci Králové'),
    'jihlava': ('Jihlava', 'v Jihlavě'),
    'karlovy-vary': ('Karlovy Vary', 'v Karlových Varech'),
    'liberec': ('Liberec', 'v Liberci'),
    'olomouc': ('Olomouc', 'v Olomouci'),
    'ostrava': ('Ostrava', 'v Ostravě'),
    'pardubice': ('Pardubice', 'v Pardubicích'),
    'plzen': ('Plzeň', 'v Plzni'),
    'usti-nad-labem': ('Ústí nad Labem', 'v Ústí nad Labem'),
    'zlin': ('Zlín', 've Zlíně'),

    # countries alphabetically
    'germany': ('Německo', 'v Německu'),
    'poland': ('Polsko', 'v Polsku'),
    'austria': ('Rakousko', 'v Rakousku'),
    'slovakia': ('Slovensko', 'na Slovensku'),
}


app = Flask(__name__)


def redirect(url):
    return render_template('meta_redirect.html', url=url)


@app.route('/')
def index():
    with db:
        jobs_count = Job.count()
        companies_count = Job.companies_count()
    return render_template('index.html',
                           nav_tabs=None,
                           jobs_count=jobs_count,
                           companies_count=companies_count,
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
        jobs_count = Job.count()
        companies_count = Job.companies_count()
        supporters_count = Supporter.count()
        last_modified = LastModified.get_value_by_path('candidate_handbook.html')
        logos = Logo.listing()
    return render_template('candidate_handbook.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='candidate_handbook',
                           jobs_count=jobs_count,
                           companies_count=companies_count,
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
    regions = [(r_id, r_name) for r_id, (r_name, r_name_in) in REGIONS.items()]
    with db:
        jobs = Job.listing()
        jobs_count = Job.count()
        companies_count = Job.companies_count()
    return render_template('jobs.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           jobs_count=jobs_count,
                           companies_count=companies_count,
                           regions=regions,
                           thumbnail=thumbnail(title='Práce v\u00a0IT pro začátečníky'))


@app.route('/jobs/region/<region_id>/')
def jobs_region(region_id):
    region_name, region_name_in = REGIONS[region_id]
    regions = [(r_id, r_name) for r_id, (r_name, r_name_in) in REGIONS.items()]
    with db:
        jobs = Job.region_listing(region_name)
    return render_template('jobs_region.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           region_id=region_id,
                           region_name=region_name,
                           region_name_in=region_name_in,
                           regions=regions,
                           thumbnail=thumbnail(title=f'Práce v\u00a0IT pro začátečníky —\u00a0{region_name}'))


@app.route('/jobs/<job_id>/')
def job(job_id):
    with db:
        job = Job.get_by_id(job_id) or abort(404)
        jobs_count = Job.count()
        companies_count = Job.companies_count()
    return render_template('job.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           job=job,
                           jobs_count=jobs_count,
                           companies_count=companies_count,
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
