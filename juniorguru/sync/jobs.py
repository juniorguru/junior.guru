from juniorguru.lib.timer import measure
from juniorguru.models import with_db
from juniorguru.lib import loggers


logger = loggers.get('jobs')


@measure('jobs')
@with_db
def main():
    # musi umet pracovat s tim, ze jsou data odminule
    # musi umet pracovat s tim, ze jsou data odminule, uz probehl sync-jobs jednou a ted se spustil znova aby syncnul increment
    # vcucne scripts/check_scrapers.py
    logger.warning('Syncing jobs not implemented yet!')


if __name__ == '__main__':
    main()
