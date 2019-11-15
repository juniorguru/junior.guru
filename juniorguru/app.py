import sys
import pickle
import warnings
from pathlib import Path

import arrow
from flask import Flask, render_template
import flask_frozen


app = Flask('juniorguru')

app.config['DATA_DIR'] = Path(app.root_path) / '..' / 'data'
app.config['BUILD_DIR'] = Path(app.root_path) / '..' / 'build'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/learn/')
def learn():
    return render_template('learn.html', year=arrow.utcnow().year)


@app.route('/practice/')
def practice():
    return render_template('practice.html')


@app.route('/jobs/')
def jobs():
    jobs_data_path = app.config['DATA_DIR'].joinpath('jobs.pickle')
    jobs = pickle.loads(jobs_data_path.read_bytes())
    return render_template('jobs.html', jobs=jobs)


@app.route('/privacy/')
def privacy():
    return render_template('privacy.html')


@app.context_processor
def inject_updated_at():
    return dict(updated_at=arrow.utcnow())


from juniorguru import template_filters  # noqa


if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'junior.guru'
    app.config['FREEZER_DESTINATION'] = app.config['BUILD_DIR']
    app.config['FREEZER_BASE_URL'] = 'https://junior.guru'
    app.config['FREEZER_STATIC_IGNORE'] = ['src']
    app.config['FREEZER_DESTINATION_IGNORE'] = ['now.json']

    warnings.filterwarnings('error', category=flask_frozen.FrozenFlaskWarning)

    freezer = flask_frozen.Freezer(app)
    freezer.freeze()
