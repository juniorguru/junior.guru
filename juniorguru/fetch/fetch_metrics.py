import os

from juniorguru.fetch.lib.google_analytics import (
    GoogleAnalyticsClient, get_daily_date_range, get_monthly_date_range,
    metric_applications_per_job, metric_avg_monthly_pageviews,
    metric_avg_monthly_users, metric_pageviews_per_external_job,
    metric_pageviews_per_job, metric_users_per_external_job,
    metric_users_per_job)
from juniorguru.fetch.lib.mailchimp import (MailChimpClient, get_collection,
                                            get_link,
                                            sum_clicks_per_external_url)
from juniorguru.models import GlobalMetric, Job, JobMetric, db


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')


def main():
    google_analytics_metrics = fetch_from_google_analytics()
    mailchimp_metrics = fetch_from_mailchimp()

    with db:
        GlobalMetric.drop_table()
        GlobalMetric.create_table()

        GlobalMetric.create(name='avg_monthly_users',
                            value=google_analytics_metrics['avg_monthly_users'])
        GlobalMetric.create(name='avg_monthly_pageviews',
                            value=google_analytics_metrics['avg_monthly_pageviews'])
        GlobalMetric.create(name='subscribers',
                            value=mailchimp_metrics['subscribers'])

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

        GlobalMetric.create(name='avg_daily_users_per_job',
                            value=JobMetric.calc_avg_daily_per_job('users'))
        GlobalMetric.create(name='avg_daily_pageviews_per_job',
                            value=JobMetric.calc_avg_daily_per_job('pageviews'))
        GlobalMetric.create(name='avg_daily_applications_per_job',
                            value=JobMetric.calc_avg_daily_per_job('applications'))


def fetch_from_google_analytics():
    api = GoogleAnalyticsClient(GOOGLE_ANALYTICS_VIEW_ID)
    metrics = {}
    metrics.update(api.execute(get_monthly_date_range(4), [
        metric_avg_monthly_users,
        metric_avg_monthly_pageviews,
    ]))
    metrics.update(api.execute(get_daily_date_range(), [
        metric_users_per_job,
        metric_users_per_external_job,
        metric_pageviews_per_job,
        metric_pageviews_per_external_job,
        metric_applications_per_job,
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
