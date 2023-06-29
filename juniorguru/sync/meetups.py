# import ics
# import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers


FEEDS = [
    'https://pyvo.cz/api/pyvo.ics',
    'https://www.meetup.com/reactgirls/events/ical/',
    'https://www.meetup.com/frontendisti/events/ical/',
]


# https://www.meetup.com/api/general/#graphQl-introduction
# https://pypi.org/project/meetup-api/


logger = loggers.from_path(__file__)


@cli.sync_command()  # TODO waiting until meetup.com decides to approve my oauth client :(
def main():
    pass
    # for feed_url in FEEDS:
    #     logger.info(f'Fetching {feed_url}')
    #     response = requests.get(feed_url, headers={'User-Agent': 'JuniorGuruBot (+https://junior.guru)'})
    #     response.raise_for_status()
    #     calendar_text = response.text.strip()
    #     if calendar_text:
    #         calendar = ics.Calendar(calendar_text)
    #         for event in calendar.events:
    #             print(event)
