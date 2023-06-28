import ics
import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers


FEEDS = [
    'https://pyvo.cz/api/pyvo.ics',
    'https://www.meetup.com/reactgirls/events/ical/',
    'https://www.meetup.com/frontendisti/events/ical/',
]


logger = loggers.from_path(__file__)


@cli.sync_command()
def main():
    for feed_url in FEEDS:
        logger.info(f'Fetching {feed_url}')
        calendar = ics.Calendar(requests.get(feed_url).text)
        for event in calendar.events:
            print(event)
