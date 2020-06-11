import os

from juniorguru.fetch.lib.google_analytics import (
    GoogleAnalyticsClient, get_date_range, metric_apply_per_job,
    metric_avg_monthly_pageviews, metric_avg_monthly_users,
    metric_pageviews_per_external_job, metric_pageviews_per_job,
    metric_users_per_external_job, metric_users_per_job)
from juniorguru.fetch.lib.mailchimp import (MailChimpClient, get_collection,
                                            get_link,
                                            sum_clicks_per_external_url)
from juniorguru.models import Metric, db


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')


def main():
    google_analytics_metrics = fetch_from_google_analytics()
    mailchimp_metrics = fetch_from_mailchimp()

    from pprint import pprint
    pprint(google_analytics_metrics)
    pprint(mailchimp_metrics)

    # save to DB
    with db:
        Metric.drop_table()
        Metric.create_table()

        # TODO
        # Metric.create(name='avg_monthly_users', value=avg_monthly_users)
        # Metric.create(name='avg_monthly_pageviews', value=avg_monthly_pageviews)
        # Metric.create(name='subscribers', value=subscribers)


def fetch_from_google_analytics():
    api = GoogleAnalyticsClient(GOOGLE_ANALYTICS_VIEW_ID)
    metrics = {}
    metrics.update(api.execute(get_date_range(4), [
        metric_avg_monthly_users,
        metric_avg_monthly_pageviews,
    ]))
    metrics.update(api.execute(get_date_range(12), [
        metric_users_per_job,
        metric_users_per_external_job,
        metric_pageviews_per_job,
        metric_pageviews_per_external_job,
        metric_apply_per_job,
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


if __name__ == '__main__':
    main()
