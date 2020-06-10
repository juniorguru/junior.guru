import json
import math
import os
from datetime import date, timedelta
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta

from juniorguru.fetch import google
from juniorguru.models import Metric, db


# Useful docs & tools:
#
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
# https://developers.google.com/analytics/devguides/reporting/core/v4/basics
# https://ga-dev-tools.appspot.com/


GOOGLE_ANALYTICS_VIEW_ID = '198392474'  # https://ga-dev-tools.appspot.com/account-explorer/
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')


def main():
    # Google Analytics
    #
    # https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
    # https://developers.google.com/analytics/devguides/reporting/core/v4/basics
    # https://ga-dev-tools.appspot.com/
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    api = google.get_client('analyticsreporting', 'v4', scope)

    date_range = get_date_range(4)

    query = prepare_monthly_values_query(GOOGLE_ANALYTICS_VIEW_ID, date_range, 'ga:users')
    monthly_data = api.reports().batchGet(body=query).execute()
    avg_monthly_users = calc_avg_monthly_values(monthly_data)

    query = prepare_monthly_values_query(GOOGLE_ANALYTICS_VIEW_ID, date_range, 'ga:pageviews')
    monthly_data = api.reports().batchGet(body=query).execute()
    avg_monthly_pageviews = calc_avg_monthly_values(monthly_data)

    query = prepare_events_query(GOOGLE_ANALYTICS_VIEW_ID, date_range, 'apply')
    events_data = api.reports().batchGet(body=query).execute()
    apply_clicks = events_data_to_dict(events_data)

    query = prepare_events_query(GOOGLE_ANALYTICS_VIEW_ID, date_range, 'job')
    events_data = api.reports().batchGet(body=query).execute()
    job_clicks = events_data_to_dict(events_data)

    # MailChimp
    #
    # https://mailchimp.com/help/about-api-keys/
    # https://mailchimp.com/developer/guides/get-started-with-mailchimp-api-3/
    url_base = 'https://us3.api.mailchimp.com/3.0'
    session = requests.Session()
    session.auth = ('junior.guru', MAILCHIMP_API_KEY)

    response = session.get(f'{url_base}/lists/')
    response.raise_for_status()
    list_ = [list_ for list_ in response.json()['lists']
             if list_['name'] == 'junior.guru'][0]
    subscribers = list_['stats']['member_count']

    # save to DB
    with db:
        Metric.drop_table()
        Metric.create_table()

        Metric.create(name='avg_monthly_users', value=avg_monthly_users)
        Metric.create(name='avg_monthly_pageviews', value=avg_monthly_pageviews)
        Metric.create(name='subscribers', value=subscribers)


def get_date_range(months, today=None):
    today = today or date.today()
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    return (
        today - relativedelta(day=1, months=months),
        today - relativedelta(day=last_day_last_month.day, months=1)
    )


def calc_avg_monthly_values(monthly_data):
    total = int(monthly_data['reports'][0]['data']['totals'][0]['values'][0])
    months = monthly_data['reports'][0]['data']['rowCount']
    return int(math.ceil(total / months))


def prepare_monthly_values_query(view_id, date_range, metric):
    return {
        'reportRequests': [
            {
                'viewId': view_id,
                'dateRanges': [
                    {
                        'startDate': date_range[0].isoformat(),
                        'endDate': date_range[1].isoformat()
                    }
                ],
                'metrics': [{'expression': metric}],
                'dimensions': [{'name': 'ga:month'}],
            },
        ],
    }


def prepare_events_query(view_id, date_range, category):
    return {
        'reportRequests': [
            {
                'viewId': view_id,
                'dateRanges': [
                    {
                        'startDate': date_range[0].isoformat(),
                        'endDate': date_range[1].isoformat()
                    },
                ],
                'metrics': [
                    {'expression': 'ga:uniqueEvents'}
                ],
                'dimensionFilterClauses': [{
                    'filters': [{
                        'dimensionName': 'ga:eventCategory',
                        'operator': 'EXACT',
                        'expressions': [category],
                    }],
                }],
                'dimensions': [
                    {'name': 'ga:eventLabel'}
                ],
            },
        ],
    }


def events_data_to_dict(events_data):
    return {
        row['dimensions'][0]: int(row['metrics'][0]['values'][0])
        for row in events_data['reports'][0]['data']['rows']
    }


if __name__ == '__main__':
    main()
