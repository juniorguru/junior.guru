from juniorguru.lib import loggers
from juniorguru.lib import timer
# from juniorguru.sync.metrics import main as sync_metrics
# from juniorguru.sync.jobs_club import main as sync_jobs_club
# from juniorguru.lib.ai import set_ai_opinion


PACKAGE_NAME = __loader__.name[:-len('.__main__')]


logger = loggers.get(PACKAGE_NAME)


@timer.notify
@timer.measure(f'{PACKAGE_NAME}.main')
def main():
    # TODO sync_metrics()  # depends on jobs, logos, transactions
    # TODO set_ai_opinion()  # depends on employments
    # TODO sync_jobs_club()  # depends on employments, jobs, club_content (in the future: set_ai_opinion)
    pass


main()
logger.info('Synchronization done!')
