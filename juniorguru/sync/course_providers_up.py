import requests

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=[])  # TODO
def main():
    courses = []
    start = 0
    step = 100
    while True:
        logger.info(f'Fetching courses from {start} to {start + step}')
        response = requests.post('https://www.uradprace.cz/rekvalifikace/rest/kurz/query', json={
            "index": ["rekvalifikace"],
            "pagination": {
                "start": start,
                "count": step,
                "order": ["-id"]
            },
            "query": {
                "must": [
                    {"match": {"field": "kategorie.kategorieId", "query": 10115}},
                ]
            }
        })
        response.raise_for_status()
        response_list = response.json()['list']
        if response_list:
            courses.extend(response_list)
            start += step
        else:
            break
    logger.info(f'Downloaded {len(courses)} courses in total')
