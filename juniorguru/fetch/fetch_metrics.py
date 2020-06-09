import json
import math
import os
from datetime import date, timedelta
from pathlib import Path

from apiclient.discovery import build
from dateutil.relativedelta import relativedelta
from oauth2client.service_account import ServiceAccountCredentials

from juniorguru.models import Metric, db


# The following URLs describe how to work with the Google Analytics Reporting API v4:
# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
# https://developers.google.com/analytics/devguides/reporting/core/v4/basics
#
# At the time of writing this comment, there is also API v3 and it took
# immense effort to find those URLs. Of course no doubt the URLs will stop
# working in about a week or two.


# Apparently an ID of the project. Per Google's docs I got it from the API
# itself using the https://ga-dev-tools.appspot.com/account-explorer/
VIEW_ID = '198392474'


def main():
    sa_path = Path(__file__).parent / 'google_service_account.json'
    sa_json = os.getenv('GOOGLE_SERVICE_ACCOUNT') or sa_path.read_text()
    sa = json.loads(sa_json)
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(sa, scope)

    range_months = get_range_months(6)

    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    avg_monthly_users = calc_avg_monthly_users(analytics.reports().batchGet(
        body={
            'reportRequests': [
                {'viewId': VIEW_ID,
                 'dateRanges': [
                     {'startDate': range_months[0].isoformat(),
                     'endDate': range_months[1].isoformat()}],
                 'metrics': [{'expression': 'ga:users'}],
                 'dimensions': [{'name': 'ga:month'}]},
            ]
        }
    ).execute())

    with db:
        Metric.drop_table()
        Metric.create_table()

        Metric.create(name='avg_monthly_users', value=avg_monthly_users)


def get_range_months(months, today=None):
    today = today or date.today()
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    return (
        today - relativedelta(day=1, months=months),
        today - relativedelta(day=last_day_last_month.day, months=1)
    )


def calc_avg_monthly_users(api_response):
    total = int(api_response['reports'][0]['data']['totals'][0]['values'][0])
    months = api_response['reports'][0]['data']['rowCount']
    return math.ceil(total / months)


if __name__ == '__main__':
    main()
