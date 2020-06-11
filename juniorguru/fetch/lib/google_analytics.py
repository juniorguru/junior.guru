import math
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from juniorguru.fetch.lib.google import get_client


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
        'dateRanges': [
            {
                'startDate': date_range[0].isoformat(),
                'endDate': date_range[1].isoformat(),
            }
        ],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:month'}],
    }
    yield calc_avg_monthly_values(report)


def metric_avg_monthly_pageviews(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [
            {
                'startDate': date_range[0].isoformat(),
                'endDate': date_range[1].isoformat(),
            }
        ],
        'metrics': [{'expression': 'ga:pageviews'}],
        'dimensions': [{'name': 'ga:month'}],
    }
    yield calc_avg_monthly_values(report)


def metric_users_per_external_url(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [
            {
                'startDate': date_range[0].isoformat(),
                'endDate': date_range[1].isoformat(),
            },
        ],
        'metrics': [
            {'expression': 'ga:uniqueEvents'}
        ],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:eventCategory',
                'operator': 'EXACT',
                'expressions': ['job'],
            }],
        }],
        'dimensions': [
            {'name': 'ga:eventLabel'}
        ],
    }
    yield events_report_to_dict(report)


def metric_apply_per_url(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [
            {
                'startDate': date_range[0].isoformat(),
                'endDate': date_range[1].isoformat(),
            },
        ],
        'metrics': [
            {'expression': 'ga:uniqueEvents'}
        ],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:eventCategory',
                'operator': 'EXACT',
                'expressions': ['apply'],
            }],
        }],
        'dimensions': [
            {'name': 'ga:eventLabel'}
        ],
    }
    yield events_report_to_dict(report)


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


def events_report_to_dict(events_report):
    return {
        row['dimensions'][0]: int(row['metrics'][0]['values'][0])
        for row in events_report['data']['rows']
    }
