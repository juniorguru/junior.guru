import os
import sys
import time
import json
from operator import itemgetter
from itertools import groupby
from subprocess import run
from urllib import request


POLLING_WAIT_S = 15
POLLING_TIMEOUT_S = 900  # 15min
POLLING_END_CONTEXT = 'ci/circleci: fetch-build'

GITHUB_ORG = os.getenv('NOW_GITHUB_COMMIT_ORG')
GITHUB_REPO = os.getenv('NOW_GITHUB_COMMIT_REPO')
GITHUB_SHA = os.getenv('NOW_GITHUB_COMMIT_SHA')


def now_github_build():
    statuses_url = ('https://api.github.com'
                    f'/repos/{GITHUB_ORG}/{GITHUB_REPO}/commits/{GITHUB_SHA}/statuses')
    release_url = None

    t = time.time()
    while True:
        print(f"Checking the '{POLLING_END_CONTEXT}' status...", flush=True)
        data = json.loads(request.urlopen(statuses_url).read())

        print('Statuses:')
        for context, state, url in aggregate_statuses(data):
            print(f"\t{context} - {state}")
            if context == POLLING_END_CONTEXT and state == 'success':
                release_url = url

        if release_url:
            print('Done!', flush=True)
            break

        if time.time() - t > POLLING_TIMEOUT_S:
            print('Timeout!', flush=True)
            sys.exit(1)

        print(f'Waiting {POLLING_WAIT_S} more seconds...', end='\n\n', flush=True)
        time.sleep(POLLING_WAIT_S)

    print('Downloading artifact...')
    release_url = release_url.split('?')[0]  # https://circleci.com/gh/honzajavorek/junior.guru/3558
    release_url = release_url.replace('https://circleci.com/', 'https://circleci.com/api/v1.1/project/')
    release_url += '/artifacts'

    req = request.Request(url=release_url,
                          headers={'Accept': 'application/json'})
    artifacts = json.loads(request.urlopen(req).read())
    request.urlretrieve(artifacts[0]['url'], 'public.tar.gz')

    print('Unpacking artifact...')
    os.makedirs('public', exist_ok=True)
    run(['tar', '-xvzf', 'public.tar.gz'])  # TODO https://askubuntu.com/a/1076825


def aggregate_statuses(statuses):
    all_statuses = sorted(statuses, key=itemgetter('context'))
    for context, context_statuses in groupby(all_statuses, key=itemgetter('context')):
        sorted_context_statuses = sorted(context_statuses, key=itemgetter('updated_at'), reverse=True)
        last_status = sorted_context_statuses[0]
        yield (context, last_status['state'], last_status['target_url'])


def now_dev_build():
    run(['pipenv', 'run', 'fetch'])
    run(['pipenv', 'run', 'build'])


if __name__ == '__main__':
    # triggered by GitHub, runs inside Now
    if os.getenv('NOW_GITHUB_DEPLOYMENT'):
        now_github_build()

    # triggered by CI nightly build, runs inside Now, the 'public' directory
    # should be already populated from the CI build
    elif os.getenv('NOW_BUILDER'):
        pass

    # triggered manually, runs locally
    else:
        now_dev_build()
