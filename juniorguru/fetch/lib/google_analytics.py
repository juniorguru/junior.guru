import math
from datetime import date, timedelta
from urllib.parse import urlparse

from dateutil.relativedelta import relativedelta

from juniorguru.fetch.lib.google import get_client
from juniorguru.url_params import strip_params


class GoogleAnalyticsClient():
    # Useful links:
    #
    # https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
    # https://developers.google.com/analytics/devguides/reporting/core/v4/basics
    # https://ga-dev-tools.appspot.com/

    def __init__(self, view_id):
        self.view_id = view_id
        self.client = get_client('analyticsreporting', 'v4', [
            'https://www.googleapis.com/auth/analytics.readonly',
        ])

    def execute(self, date_range, metric_fns):
        # prepare generators
        metric_fns = [fn(self.view_id, date_range) for fn in metric_fns]

        # let them generate report requests
        body = {'reportRequests': [next(fn) for fn in metric_fns]}

        # request the API
        data = self.client.reports().batchGet(body=body).execute()

        # feed the generators with the response, let them generate the metric
        metrics = {}
        for i, fn in enumerate(metric_fns):
            name = fn.__name__.replace('metric_', '')
            value = fn.send(data['reports'][i])
            metrics[name] = value
        return metrics


def metric_avg_monthly_users(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:month'}],
    }
    yield calc_avg_monthly_values(report)


def metric_avg_monthly_pageviews(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:pageviews'}],
        'dimensions': [{'name': 'ga:month'}],
    }
    yield calc_avg_monthly_values(report)


def metric_users_per_job(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:pagePath'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/jobs/[^/]+/'],
            }],
        }],
        'orderBys': [{
            'fieldName': 'ga:users',
            'sortOrder': 'DESCENDING',
        }]
    }
    yield {f'https://junior.guru{url}': value for url, value
           in per_url_report_to_dict(report).items()}


def metric_pageviews_per_job(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:pageviews'}],
        'dimensions': [{'name': 'ga:pagePath'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/jobs/[^/]+/'],
            }],
        }],
        'orderBys': [{
            'fieldName': 'ga:pageviews',
            'sortOrder': 'DESCENDING',
        }]
    }
    yield {f'https://junior.guru{url}': value for url, value
           in per_url_report_to_dict(report).items()}


def metric_users_per_external_job(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:uniqueEvents'}],
        'dimensions': [{'name': 'ga:eventLabel'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:eventCategory',
                'operator': 'EXACT',
                'expressions': ['job'],
            }],
        }],
    }
    yield per_url_report_to_dict(report)


def metric_pageviews_per_external_job(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:totalEvents'}],
        'dimensions': [{'name': 'ga:eventLabel'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:eventCategory',
                'operator': 'EXACT',
                'expressions': ['job'],
            }],
        }],
    }
    yield per_url_report_to_dict(report)


def metric_apply_per_job(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:uniqueEvents'}],
        'dimensions': [{'name': 'ga:eventLabel'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:eventCategory',
                'operator': 'EXACT',
                'expressions': ['apply'],
            }],
        }],
    }
    yield per_url_report_to_dict(report)


def get_date_range(months, today=None):
    today = today or date.today()
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    return (
        today - relativedelta(day=1, months=months),
        today - relativedelta(day=last_day_last_month.day, months=1)
    )


def calc_avg_monthly_values(monthly_report):
    total = int(monthly_report['data']['totals'][0]['values'][0])
    months = monthly_report['data']['rowCount']
    return int(math.ceil(total / months))


def per_url_report_to_dict(events_report):
    data = {}
    for row in events_report['data']['rows']:
        url = strip_params(row['dimensions'][0], 'fbclid')
        value = int(row['metrics'][0]['values'][0])
        data.setdefault(url, 0)
        data[url] += value
    return data
