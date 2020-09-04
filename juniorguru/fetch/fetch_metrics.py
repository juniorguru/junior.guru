import os

from juniorguru.fetch.lib.google_analytics import (
    GoogleAnalyticsClient, get_daily_date_range,
    metric_applications_per_job, metric_avg_monthly_pageviews,
    metric_avg_monthly_users, metric_pageviews_per_external_job,
    metric_pageviews_per_job, metric_users_per_external_job,
    metric_users_per_job, metric_locations_per_job, metric_avg_monthly_handbook_users,
    metric_avg_monthly_handbook_pageviews, metric_avg_monthly_handbook_logo_clicks)
from juniorguru.fetch.lib.mailchimp import (MailChimpClient, get_collection,
                                            get_link,
                                            sum_clicks_per_external_url)
from juniorguru.models import Job, JobMetric, Metric, db


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')


def main():
    google_analytics_metrics = fetch_from_google_analytics()
    mailchimp_metrics = fetch_from_mailchimp()

    with db:
        Metric.drop_table()
        Metric.create_table()

        google_analytics_metric_names = [
            'avg_monthly_users',
            'avg_monthly_pageviews',
            'avg_monthly_handbook_users',
            'avg_monthly_handbook_pageviews',
            'avg_monthly_handbook_logo_clicks',
        ]
        for name in google_analytics_metric_names:
            Metric.create(name=name, value=google_analytics_metrics[name])

        Metric.create(name='avg_monthly_handbook_conversion', value=(
            (google_analytics_metrics['avg_monthly_handbook_logo_clicks'] /
             google_analytics_metrics['avg_monthly_handbook_users']) * 100
        ))
        Metric.create(name='subscribers', value=mailchimp_metrics['subscribers'])

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

        users_per_external_url = merge_metric_dicts(
            google_analytics_metrics['users_per_external_job'],
            mailchimp_metrics['users_per_external_url']
        )
        for url, value in users_per_external_url.items():
            try:
                job = Job.get_by_link(url)
                JobMetric.create(job=job, name='users', value=value)
            except Job.DoesNotExist:
                pass

        pageviews_per_external_url = merge_metric_dicts(
            google_analytics_metrics['pageviews_per_external_job'],
            mailchimp_metrics['pageviews_per_external_url']
        )
        for url, value in pageviews_per_external_url.items():
            try:
                job = Job.get_by_link(url)
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
    ]))
    metrics.update(api.execute(get_daily_date_range(), [
        metric_users_per_job,
        metric_users_per_external_job,
        metric_pageviews_per_job,
        metric_pageviews_per_external_job,
        metric_applications_per_job,
        metric_locations_per_job,
        # metric_users_per_logo,
        # metric_pageviews_per_logo,
        # metric_clicks_per_logo,
    ]))
    return metrics


def fetch_from_mailchimp():
    metrics = {}

    api = MailChimpClient(MAILCHIMP_API_KEY)
    lists = get_collection(api.get('/lists/', count=1), 'lists')
    metrics['subscribers'] = lists[0]['stats']['member_count']

    urls_clicked = []
    reports = get_collection(api.get('/reports/', count=1000), 'reports')
    for report in reports:
        url = get_link(report, 'click-details')
        data = api.get(url, count=1000)
        urls_clicked.extend(get_collection(data, 'urls_clicked'))

    metrics['users_per_external_url'] = sum_clicks_per_external_url(urls_clicked, 'unique_clicks')
    metrics['pageviews_per_external_url'] = sum_clicks_per_external_url(urls_clicked, 'total_clicks')
    return metrics


def merge_metric_dicts(metric_dict1, metric_dict2):
    metric_dict = dict(metric_dict1)
    for url, value in metric_dict2.items():
        metric_dict.setdefault(url, 0)
        metric_dict[url] += value
    return metric_dict


if __name__ == '__main__':
    main()
