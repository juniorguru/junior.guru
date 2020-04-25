import re
import json
from pathlib import Path

from playhouse.shortcuts import model_to_dict
from flask import render_template, send_from_directory

from . import app
from ..models import db, Job
from juniorguru.scrapers.settings import MONITORING_EXPORT_DIR


ADMIN_MENU = {
    'Záložky': 'admin',
    'Newsletter': 'admin_newsletter',
    'Stažené nabídky v DB': 'admin_scraped_jobs',
    'Stažené nabídky': 'admin_scraped_items',
    'Zahozené nabídky': 'admin_drops',
    'Chyby': 'admin_errors',
}


def load_scrapers_monitoring(export_dir, basename):
    path = Path(export_dir) / basename
    try:
        return None, json.loads(path.read_text())
    except (IOError, json.JSONDecodeError) as load_error:
        return load_error, []


@app.route('/admin/')
def admin():
    return render_template('admin.html')


@app.route('/admin/newsletter/')
def admin_newsletter():
    with db:
        jobs = Job.newsletter_listing()
    return render_template('admin_newsletter.html', jobs=jobs)


@app.route('/admin/scraped-jobs/')
def admin_scraped_jobs():
    with db:
        jobs = [model_to_dict(job) for job in Job.scraped_listing()]
    return render_template('admin_scraped_jobs.html', jobs=jobs)


@app.route('/admin/scraped-items/')
def admin_scraped_items():
    load_error, items = load_scrapers_monitoring(MONITORING_EXPORT_DIR,
                                                 'items.json')
    items = sorted(items, key=lambda d: d['posted_at'], reverse=True)
    return render_template('admin_scraped_items.html',
                           load_error=load_error,
                           items=items)


@app.route('/admin/dropped-items/')
def admin_drops():
    load_error, drops = load_scrapers_monitoring(MONITORING_EXPORT_DIR,
                                                 'drops.json')
    drops = sorted(drops, key=lambda d: d['item']['posted_at'], reverse=True)
    return render_template('admin_drops.html',
                           load_error=load_error,
                           drops=drops)


@app.route('/admin/errors/')
def admin_errors():
    load_error, errors = load_scrapers_monitoring(MONITORING_EXPORT_DIR,
                                                 'errors.json')
    def sort_key(error):
        try:
            return error['item']['posted_at']
        except KeyError:
            return error['message']

    return render_template('admin_errors.html',
                           load_error=load_error,
                           errors=sorted(errors, key=sort_key, reverse=True))


@app.route('/admin/debug/<path:path>.txt')
def admin_debug(path):
    debug_dir = Path(MONITORING_EXPORT_DIR).absolute()
    return send_from_directory(debug_dir, path, mimetype='text/plain')


@app.context_processor
def inject_admin():
    return dict(admin_menu=ADMIN_MENU)
