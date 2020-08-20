import arrow
from flask import Flask, Response, abort, render_template, url_for

from juniorguru.models import Job, Metric, Story, Supporter, db
from juniorguru.web.thumbnail import thumbnail


NAV_TABS = [
    {'endpoint': 'learn', 'name': 'Nauč se základy', 'name_short': 'Základy'},
    {'endpoint': 'practice', 'name': 'Získej praxi', 'name_short': 'Praxe'},
    {'endpoint': 'jobs', 'name': 'Najdi práci', 'name_short': 'Práce'},
]

JOBS_SUBNAV_TABS = [
    {'endpoint': 'jobs', 'name': 'Nabídky práce'},
    {'endpoint': 'candidate_handbook_teaser', 'name': 'Příručka hledání práce'},
    {'endpoint': 'hire_juniors', 'name': 'Pro firmy'},
]


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


@app.route('/candidate/')
def candidate():
    return redirect(url_for('candidate_handbook_teaser', _external=True))


@app.route('/candidate-handbook/')
def candidate_handbook_teaser():
    with db:
        metrics = Metric.as_dict()
    return render_template('candidate_handbook_teaser.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='candidate_handbook_teaser',
                           metrics=metrics,
                           thumbnail=thumbnail(title='Příručka hledání první práce v\u00a0IT'))


@app.route('/__supercalifragilisticexpialidocious__/')
def candidate_handbook():
    with db:
        jobs_count = Job.count()
        companies_count = Job.companies_count()
        supporters_count = Supporter.count()
    return render_template('candidate_handbook.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='candidate_handbook_teaser',
                           jobs_count=jobs_count,
                           companies_count=companies_count,
                           supporters_count=supporters_count,
                           thumbnail=thumbnail(title='Příručka hledání první práce v\u00a0IT'))


@app.route('/jobs/')
def jobs():
    with db:
        jobs = Job.listing()
        jobs_count = Job.count()
        companies_count = Job.companies_count()
        jobs_bot = Job.bot_listing()
    return render_template('jobs.html',
                           nav_active='jobs',
                           subnav_tabs=JOBS_SUBNAV_TABS,
                           subnav_active='jobs',
                           jobs=jobs,
                           jobs_count=jobs_count,
                           companies_count=companies_count,
                           jobs_bot=jobs_bot,
                           thumbnail=thumbnail(title='Práce v\u00a0IT pro začátečníky'))


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
                updated_at=now,
                thumbnail=thumbnail())


from juniorguru.web import admin, template_filters  # noqa
