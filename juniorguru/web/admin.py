from flask import render_template, send_from_directory
from playhouse.shortcuts import model_to_dict

from juniorguru.models import Job, JobDropped, JobError, Metric, db, SpiderMetric
from juniorguru.jobs.legacy_jobs.monitoring import RESPONSES_BACKUP_DIR
from juniorguru.web import app


ADMIN_NAV = {
    'Rozcestník': 'admin',
    'Nabídky': 'admin_jobs',
    'Zahozené nabídky': 'admin_jobs_dropped',
    'Chyby v nabídkách': 'admin_jobs_errors',
}


def models_to_dicts(objects):
    return list(map(model_to_dict, objects))


def models_to_dicts_with_metrics(objects):
    return [dict(metrics=obj.metrics,
                 location=obj.location,
                 **model_to_dict(obj)) for obj in objects]


@app.route('/a/')
def admin():
    with db:
        metrics = Metric.as_dict()
    return render_template('admin.html', metrics=metrics)


@app.route('/a/jobs/')
def admin_jobs():
    with db:
        jobs = models_to_dicts_with_metrics(Job.listing())
    return render_template('admin_jobs.html', jobs=jobs)


@app.route('/a/jobs/dropped/')
def admin_jobs_dropped():
    with db:
        jobs_dropped = JobDropped.admin_listing(['NotEntryLevel'])
    return render_template('admin_jobs_dropped.html',
                           title='Nejuniorní zahozené nabídky',
                           jobs_dropped=models_to_dicts(jobs_dropped))


@app.route('/a/jobs/dropped/unexpected/')
def admin_jobs_dropped_unexpected():
    with db:
        jobs_dropped = JobDropped.admin_listing(['MissingRequiredFields', 'ShortDescription', 'MissingIdentifyingField'])
    return render_template('admin_jobs_dropped.html',
                           title='Podezřele zahozené nabídky',
                           jobs_dropped=models_to_dicts(jobs_dropped))


@app.route('/a/jobs/dropped/expected/')
def admin_jobs_dropped_expected():
    with db:
        jobs_dropped = JobDropped.admin_listing(['Expired', 'NotApproved'])
    return render_template('admin_jobs_dropped.html',
                           title='Vědomě zahozené nabídky',
                           jobs_dropped=models_to_dicts(jobs_dropped))


@app.route('/a/jobs/dropped/all/')
def admin_jobs_dropped_all():
    with db:
        jobs_dropped = JobDropped.admin_listing()
    return render_template('admin_jobs_dropped.html',
                           title='Všechny zahozené nabídky',
                           jobs_dropped=models_to_dicts(jobs_dropped))


@app.route('/a/jobs/errors/')
def admin_jobs_errors():
    with db:
        spider_metrics = SpiderMetric.as_dict()
        spider_errors = models_to_dicts(SpiderMetric.select().where(SpiderMetric.name == 'log_count/ERROR'))
        jobs_errors = models_to_dicts(JobError.admin_listing())
    return render_template('admin_jobs_errors.html', spider_metrics=spider_metrics,
                                                     spider_errors=spider_errors,
                                                     jobs_errors=jobs_errors)


@app.route('/a/responses-backup/<path:path>')
def admin_responses_backup(path):
    return send_from_directory(RESPONSES_BACKUP_DIR, path, mimetype='text/plain')


@app.context_processor
def inject_admin():
    return dict(admin_nav=ADMIN_NAV)
