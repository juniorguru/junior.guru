import math

from juniorguru.lib.timer import measure
from juniorguru.lib.google_analytics import (
    GoogleAnalyticsClient, get_daily_date_range,
    metric_applications_per_job, metric_avg_monthly_pageviews,
    metric_avg_monthly_users, metric_pageviews_per_external_job,
    metric_pageviews_per_job, metric_users_per_external_job,
    metric_users_per_job, metric_avg_monthly_handbook_users,
    metric_avg_monthly_handbook_pageviews, metric_avg_monthly_handbook_logo_clicks,
    metric_clicks_per_logo, metric_handbook_users_per_date, metric_handbook_pageviews_per_date,
    metric_avg_monthly_jobs_users)
from juniorguru.lib import google_sheets
from juniorguru.lib.coerce import parse_currency, parse_ptc
from juniorguru.models import Job, JobMetric, Metric, db


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
FINANCES_DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'


@measure('metrics')
def main():
    google_analytics_metrics = fetch_from_google_analytics()
    google_sheets_metrics = fetch_from_google_sheets()

    with db:
        Metric.drop_table()
        Metric.create_table()

        for name in [
            'avg_monthly_users',
            'avg_monthly_pageviews',
            'avg_monthly_handbook_users',
            'avg_monthly_handbook_pageviews',
            'avg_monthly_handbook_logo_clicks',
            'avg_monthly_jobs_users',
        ]:
            Metric.create(name=name, value=google_analytics_metrics[name])
        for name, value in google_sheets_metrics.items():
            Metric.create(name=name, value=value)

        JobMetric.drop_table()
        JobMetric.create_table()

        for url, value in google_analytics_metrics['users_per_job'].items():
            try:
                job = Job.get_by_url(url)
                JobMetric.create(job=job, name='users', value=value)
            except Job.DoesNotExist:
                pass

        for url, value in google_analytics_metrics['pageviews_per_job'].items():
            try:
                job = Job.get_by_url(url)
                JobMetric.create(job=job, name='pageviews', value=value)
            except Job.DoesNotExist:
                pass

        for url, value in google_analytics_metrics['applications_per_job'].items():
            try:
                job = Job.get_by_url(url)
                JobMetric.create(job=job, name='applications', value=value)
            except Job.DoesNotExist:
                pass

        for url, value in google_analytics_metrics['users_per_external_job'].items():
            try:
                job = Job.get_by_url(url)
                JobMetric.create(job=job, name='users', value=value)
            except Job.DoesNotExist:
                pass

        for url, value in google_analytics_metrics['pageviews_per_external_job'].items():
            try:
                job = Job.get_by_url(url)
                JobMetric.create(job=job, name='pageviews', value=value)
            except Job.DoesNotExist:
                pass


def fetch_from_google_analytics():
    api = GoogleAnalyticsClient(GOOGLE_ANALYTICS_VIEW_ID)
    metrics = {}
    metrics.update(api.execute(get_daily_date_range(start_months_ago=4), [
        metric_avg_monthly_users,
        metric_avg_monthly_pageviews,
        metric_avg_monthly_handbook_users,
        metric_avg_monthly_handbook_pageviews,
        metric_avg_monthly_handbook_logo_clicks,
        metric_avg_monthly_jobs_users,
    ]))
    metrics.update(api.execute(get_daily_date_range(), [
        metric_users_per_job,
        metric_users_per_external_job,
        metric_pageviews_per_job,
        metric_pageviews_per_external_job,
        metric_applications_per_job,
        metric_clicks_per_logo,
        metric_handbook_users_per_date,
        metric_handbook_pageviews_per_date,
    ]))
    return metrics


def fetch_from_google_sheets():
    cells = google_sheets.download_raw(google_sheets.get(FINANCES_DOC_KEY, 'finances'))
    return parse_finances(cells)


def parse_finances(cells):
    metrics = {}
    current_section = None
    for row in cells:
        if row[0] == 'Total Income':
            metrics['inc_total'] = math.ceil(parse_currency(row[1]))
            current_section = 'inc'
        elif row[0] == 'Total Expenses':
            metrics['exp_total'] = math.ceil(parse_currency(row[1]))
            current_section = 'exp'
        elif row[0] == 'Months':
            current_section = 'total'
        elif not any(row):
            current_section = None
        elif row[0] and current_section:
            prefix = '' if current_section == 'total' else f'{current_section}_'
            name = prefix + row[0].replace(' ', '_').lower()
            metrics[name] = math.ceil(parse_currency(row[1]))
            if row[2]:
                metrics[f'{name}_pct'] = math.ceil(parse_ptc(row[2]))
    return metrics


if __name__ == '__main__':
    main()
