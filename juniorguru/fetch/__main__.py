from .fetch_jobs import main as fetch_jobs
from .fetch_stories import main as fetch_stories


def main():
    fetch_jobs()
    fetch_stories()


if __name__ == '__main__':
    main()
