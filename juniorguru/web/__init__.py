from datetime import datetime

import arrow
from flask import Flask, render_template

from ..models import db, Job


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


@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')


@app.context_processor
def inject_updated_at():
    return dict(updated_at=arrow.utcnow())


from . import template_filters  # noqa
