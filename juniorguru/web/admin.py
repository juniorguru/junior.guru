import re
import json
from pathlib import Path

from playhouse.shortcuts import model_to_dict
from flask import render_template, send_from_directory

from juniorguru.web import app
from juniorguru.models import db, Job, JobDropped, JobError
from juniorguru.scrapers.monitoring import RESPONSES_BACKUP_DIR


ADMIN_MENU = {
    'Záložky': 'admin',
    'Newsletter': 'admin_newsletter',
    'Stažené nabídky': 'admin_jobs_scraped',
    'Zahozené nabídky': 'admin_jobs_dropped',
    'Chyby při stahování': 'admin_jobs_errors',
}


def models_to_dicts(models):
    return list(map(model_to_dict, models))


@app.route('/admin/')
def admin():
    return render_template('admin.html')


@app.route('/admin/newsletter/')
def admin_newsletter():
    with db:
        jobs = Job.newsletter_listing()
    return render_template('admin_newsletter.html', jobs=jobs)


@app.route('/admin/jobs-scraped/')
def admin_jobs_scraped():
    with db:
        jobs = models_to_dicts(Job.scraped_listing())
    return render_template('admin_jobs_scraped.html', jobs=jobs)


@app.route('/admin/jobs-dropped/')
def admin_jobs_dropped():
    with db:
        jobs_dropped = models_to_dicts(JobDropped.admin_listing())
    return render_template('admin_jobs_dropped.html', jobs_dropped=jobs_dropped)


@app.route('/admin/jobs-errors/')
def admin_jobs_errors():
    with db:
        jobs_errors = models_to_dicts(JobError.admin_listing())
    return render_template('admin_jobs_errors.html', jobs_errors=jobs_errors)


@app.route('/admin/responses-backup/<path:path>')
def admin_responses_backup(path):
    return send_from_directory(RESPONSES_BACKUP_DIR, path, mimetype='text/plain')


@app.context_processor
def inject_admin():
    return dict(admin_menu=ADMIN_MENU)
