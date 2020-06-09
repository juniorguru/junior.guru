import json
import math
import os
from datetime import date, timedelta
from pathlib import Path

from dateutil.relativedelta import relativedelta

from juniorguru.fetch import google
from juniorguru.models import Metric, db


# Useful docs & tools:
#
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
# https://developers.google.com/analytics/devguides/reporting/core/v4/basics
# https://ga-dev-tools.appspot.com/


# ID of the project - got it from the API itself using
# https://ga-dev-tools.appspot.com/account-explorer/
VIEW_ID = '198392474'


def main():
    # Google Analytics
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    api = google.get_client('analyticsreporting', 'v4', scope)

    date_range = get_date_range(4)

    body = prepare_monthly_values_query(VIEW_ID, date_range, 'ga:users')
    response = api.reports().batchGet(body=body).execute()
    avg_monthly_users = calc_avg_monthly_values(response)

    body = prepare_monthly_values_query(VIEW_ID, date_range, 'ga:pageviews')
    response = api.reports().batchGet(body=body).execute()
    avg_monthly_pageviews = calc_avg_monthly_values(response)

    # MailChimp
    # TODO

    with db:
        Metric.drop_table()
        Metric.create_table()

        Metric.create(name='avg_monthly_users', value=avg_monthly_users)
        Metric.create(name='avg_monthly_pageviews', value=avg_monthly_pageviews)


def get_date_range(months, today=None):
    today = today or date.today()
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    return (
        today - relativedelta(day=1, months=months),
        today - relativedelta(day=last_day_last_month.day, months=1)
    )


def calc_avg_monthly_values(api_response):
    total = int(api_response['reports'][0]['data']['totals'][0]['values'][0])
    months = api_response['reports'][0]['data']['rowCount']
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


if __name__ == '__main__':
    main()
