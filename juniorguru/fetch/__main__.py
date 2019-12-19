from .fetch_jobs import main as fetch_jobs
from .fetch_articles import main as fetch_articles


def main():
    fetch_jobs()
    fetch_articles()


if __name__ == '__main__':
    main()
