from datetime import datetime

import arrow
from flask import Flask, render_template, abort

from ..models import db, Job, Story
from .thumbnail import thumbnail


app = Flask(__name__)


@app.route('/')
def index():
    with db:
        jobs_count = Job.count()
        companies_count = Job.companies_count()
    return render_template('index.html',
                           jobs_count=jobs_count,
                           companies_count=companies_count,
                           since=datetime.now() - datetime(2019, 10, 10),
                           stories=Story.listing())


@app.route('/learn/')
def learn():
    return render_template('learn.html',
                           thumbnail=thumbnail(title='Jak se začít učit programovat'))


@app.route('/practice/')
def practice():
    return render_template('practice.html',
                           thumbnail=thumbnail(title='Jak získat praxi v\u00a0programování'))


@app.route('/candidate/')
def candidate():
    return render_template('candidate.html',
                           thumbnail=thumbnail(title='Jak najít první práci v IT'))


@app.route('/jobs/')
def jobs():
    with db:
        jobs = Job.listing()
        jobs_count = Job.count()
        companies_count = Job.companies_count()
    return render_template('jobs.html',
                           jobs=jobs,
                           jobs_count=jobs_count,
                           companies_count=companies_count,
                           thumbnail=thumbnail(title='Práce pro začínající programátory'))


@app.route('/jobs-newsletter.html')
def jobs_newsletter():
    with db:
        jobs = Job.newsletter_listing()
    return render_template('jobs_newsletter.html', jobs=jobs)


@app.route('/jobs/<job_id>/')
def job(job_id):
    with db:
        job = Job.get_by_id(job_id) or abort(404)
        jobs_count = Job.count()
        companies_count = Job.companies_count()
    return render_template('job.html',
                           job=job,
                           jobs_count=jobs_count,
                           companies_count=companies_count,
                           thumbnail=thumbnail(job_title=job.title,
                                               job_company=job.company_name,
                                               job_location=job.location))


@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')


@app.context_processor
def inject_defaults():
    now = arrow.utcnow()
    return dict(year=now.year,
                updated_at=now,
                thumbnail=thumbnail())


from . import template_filters  # noqa
