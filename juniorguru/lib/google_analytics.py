import math
from itertools import islice
from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta

from juniorguru.lib.google import get_client
from juniorguru.lib.url_params import strip_params


MAX_BATCH_SIZE = 5


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
        metric_fns = (fn(self.view_id, date_range) for fn in metric_fns)

        # only a number of metrics per batch is allowed by the API
        metrics = {}
        batch = list(islice(metric_fns, MAX_BATCH_SIZE))
        while batch:
            # let them generate report requests
            body = {'reportRequests': [next(fn) for fn in batch]}

            # request the API
            data = self.client.reports().batchGet(body=body).execute()

            # feed the generators with the response, let them generate the metric
            for i, fn in enumerate(batch):
                name = fn.__name__.replace('metric_', '')
                value = fn.send(data['reports'][i])
                metrics[name] = value

            # another batch
            batch = list(islice(metric_fns, MAX_BATCH_SIZE))
        return metrics


def metric_avg_monthly_users(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:date'}],
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
        'dimensions': [{'name': 'ga:date'}],
    }
    yield calc_avg_monthly_values(report)


def metric_avg_monthly_handbook_users(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:date'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/candidate-handbook/'],
            }],
        }],
    }
    yield calc_avg_monthly_values(report)


def metric_avg_monthly_handbook_pageviews(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:pageviews'}],
        'dimensions': [{'name': 'ga:date'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/candidate-handbook/'],
            }],
        }],
    }
    yield calc_avg_monthly_values(report)


def metric_avg_monthly_handbook_logo_clicks(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:uniqueEvents'}],
        'dimensions': [{'name': 'ga:date'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:eventCategory',
                'operator': 'EXACT',
                'expressions': ['handbook-logo'],
            }],
        }],
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


def metric_applications_per_job(view_id, date_range):
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


def metric_clicks_per_logo(view_id, date_range):
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
                'expressions': ['handbook-logo'],
            }],
        }],
    }
    yield per_url_report_to_dict(report)


def metric_handbook_users_per_date(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:date'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/candidate-handbook/'],
            }],
        }],
    }
    yield per_date_report_to_dict(report)


def metric_handbook_pageviews_per_date(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:pageviews'}],
        'dimensions': [{'name': 'ga:date'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/candidate-handbook/'],
            }],
        }],
    }
    yield per_date_report_to_dict(report)


def metric_avg_monthly_jobs_users(view_id, date_range):
    report = yield {
        'viewId': view_id,
        'dateRanges': [{
            'startDate': date_range[0].isoformat(),
            'endDate': date_range[1].isoformat()
        }],
        'metrics': [{'expression': 'ga:users'}],
        'dimensions': [{'name': 'ga:date'}],
        'dimensionFilterClauses': [{
            'filters': [{
                'dimensionName': 'ga:pagePath',
                'operator': 'REGEXP',
                'expressions': ['^/jobs/'],
            }],
        }],
    }
    yield calc_avg_monthly_values(report)


def get_daily_date_range(today=None, start_months_ago=None):
    today = today or date.today()
    if start_months_ago:
        start_date = today - relativedelta(days=1, months=start_months_ago)
    else:
        start_date = date(2019, 1, 1)
    return (start_date, today - timedelta(days=1))


def calc_avg_monthly_values(report):
    total = int(report['data']['totals'][0]['values'][0])
    if total == 0:
        return 0
    dates = [datetime.strptime(row['dimensions'][0], '%Y%m%d')
             for row in report['data']['rows']]
    days = (max(dates) - min(dates)).days + 1
    months = days / 30
    return int(math.ceil(total / months))


def per_url_report_to_dict(report):
    data = {}
    for row in report['data']['rows']:
        url = strip_params(row['dimensions'][0], 'fbclid')
        value = int(row['metrics'][0]['values'][0])
        data.setdefault(url, 0)
        data[url] += value
    return data


def per_date_report_to_dict(report):
    data = {}
    for row in report['data']['rows']:
        date = datetime.strptime(row['dimensions'][0], '%Y%m%d').date()
        value = int(row['metrics'][0]['values'][0])
        data.setdefault(date, 0)
        data[date] += value
    return data
