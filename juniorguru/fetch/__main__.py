from juniorguru.fetch.fetch_jobs import main as fetch_jobs
from juniorguru.fetch.fetch_metrics import main as fetch_metrics
from juniorguru.fetch.fetch_stories import main as fetch_stories


def main():
    fetch_jobs()
    fetch_stories()
    fetch_metrics()


if __name__ == '__main__':
    main()
