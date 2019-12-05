from datetime import datetime

import arrow
from flask import Flask, render_template, abort

from ..models import db, Job
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
                           since=datetime.now() - datetime(2019, 10, 10))


@app.route('/learn/')
def learn():
    return render_template('learn.html', year=arrow.utcnow().year)


@app.route('/practice/')
def practice():
    return render_template('practice.html')


@app.route('/jobs/')
def jobs():
    with db:
        jobs = Job.listing()
    return render_template('jobs.html', jobs=jobs)


@app.route('/jobs/<job_id>/')
def job(job_id):
    with db:
        job = Job.get_by_id(job_id) or abort(404)
    return render_template('job.html', job=job)


@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')


@app.context_processor
def inject_updated_at():
    return dict(updated_at=arrow.utcnow())


from . import template_filters  # noqa
