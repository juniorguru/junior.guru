import os
import sys
import time
import json
from operator import itemgetter
from itertools import groupby
from subprocess import run
from urllib import request


POLLING_WAIT_S = 15
POLLING_TIMEOUT_S = 600  # 10min
POLLING_END_CONTEXT = 'ci/circleci: release'

# NOW_GITHUB_COMMIT_ORG=honzajavorek
# NOW_GITHUB_COMMIT_REPO=junior.guru
# NOW_GITHUB_REPO=junior.guru
# NOW_GITHUB_COMMIT_AUTHOR_NAME=Honza Javorek
# NOW_GITHUB_COMMIT_AUTHOR_LOGIN=honzajavorek
# NOW_GITHUB_ORG=honzajavorek
# NOW_GITHUB_COMMIT_SHA=56b0469f3a381099644b41016e32e60e24377d5f
# NOW_GITHUB_COMMIT_REF=honzajavorek/fix-now
GITHUB_ORG = os.getenv('NOW_GITHUB_COMMIT_ORG')
GITHUB_REPO = os.getenv('NOW_GITHUB_COMMIT_REPO')
GITHUB_SHA = os.getenv('NOW_GITHUB_COMMIT_SHA')

CIRCLECI_TOKEN = os.getenv('CIRCLECI_TOKEN')


def now_github_build():
    t = time.time()
    while True:
        print('Checking statues...', flush=True)
        url = ('https://api.github.com'
               f'/repos/{GITHUB_ORG}/{GITHUB_REPO}/commits/{GITHUB_SHA}/statuses')
        data = json.loads(request.urlopen(url).read())
        statuses = dict(aggregate_statuses(data))

        print('Statuses:')
        for context, state in statuses.items():
            print(f"\t{context} - {state}")

        if statuses.get(POLLING_END_CONTEXT) == 'success':
            print('Done!', flush=True)
            break

        if time.time() - t > POLLING_TIMEOUT_S:
            print('Timeout!', flush=True)
            sys.exit(1)

        print(f'Waiting {POLLING_WAIT_S} more seconds...', end='\n\n', flush=True)
        time.sleep(POLLING_WAIT_S)


def aggregate_statuses(statuses):
    all_statuses = sorted(statuses, key=itemgetter('context'))
    for context, context_statuses in groupby(all_statuses, key=itemgetter('context')):
        sorted_context_statuses = sorted(context_statuses, key=itemgetter('updated_at'), reverse=True)
        yield (context, statuses[0]['state'])


def now_build():
    run(['pipenv', 'run', 'fetch'])
    run(['pipenv', 'run', 'build'])


if __name__ == '__main__':
    if os.getenv('NOW_GITHUB_DEPLOYMENT'):
        now_github_build()
    else:
        now_build()
