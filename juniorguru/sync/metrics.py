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
from juniorguru.models import Job, JobMetric, Metric, db


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
FINANCES_DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'


@measure()
@db.connection_context()
def main():
    google_analytics_metrics = fetch_from_google_analytics()

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


if __name__ == '__main__':
    main()
