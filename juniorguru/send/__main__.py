import sys

from juniorguru.send.job_metrics import main as send_job_metrics
from juniorguru.send.logo_metrics import main as send_logo_metrics


def main():
    sys.exit(max(
        send_logo_metrics(),
        send_job_metrics(),
    ))


if __name__ == '__main__':
    main()
