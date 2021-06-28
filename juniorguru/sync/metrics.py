import math
import os

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
from juniorguru.lib.mailchimp import (MailChimpClient, get_collection,
                                            get_link,
                                            sum_clicks_per_external_url)
from juniorguru.models import Job, JobMetric, Metric, Logo, LogoMetric, db


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
FINANCES_DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'


def main():
    google_analytics_metrics = fetch_from_google_analytics()
    google_sheets_metrics = fetch_from_google_sheets()
    mailchimp_metrics = fetch_from_mailchimp()

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

        LogoMetric.drop_table()
        LogoMetric.create_table()

        for url, value in google_analytics_metrics['clicks_per_logo'].items():
            try:
                logo = Logo.get_by_url(url)
                LogoMetric.create(logo=logo, name='clicks', value=value)
            except Logo.DoesNotExist:
                pass

        for logo in Logo.listing():
            values = google_analytics_metrics['handbook_users_per_date']
            metric = LogoMetric.from_values_per_date(logo, 'users', values)
            metric.save()
            values = google_analytics_metrics['handbook_pageviews_per_date']
            metric = LogoMetric.from_values_per_date(logo, 'pageviews', values)
            metric.save()


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


def merge_metric_dicts(metric_dict1, metric_dict2):
    metric_dict = dict(metric_dict1)
    for url, value in metric_dict2.items():
        metric_dict.setdefault(url, 0)
        metric_dict[url] += value
    return metric_dict


if __name__ == '__main__':
    main()
