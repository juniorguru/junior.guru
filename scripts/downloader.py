import asyncio
import os
from pathlib import Path

from requests import get


DOWNLOAD_DIR = Path(__file__).parent.parent / 'backups'
PROJECT_URL = 'https://circleci.com/api/v1.1/project/github/honzajavorek/junior.guru'


def is_sync_job(job):
    return job.get('workflows', {}).get('job_name', '') in ('sync', 'fetch')


def is_nightly_job(job):
    return job.get('workflows', {}).get('workflow_name', '') == 'nightly'


def is_sync_and_nightly(job):
    return is_sync_job(job) and is_nightly_job(job)


def fetch_url(build_num):
    try:
        res = get(f'{PROJECT_URL}/{build_num}/artifacts')
        res.raise_for_status()
        artifacts = list(filter(lambda artifact: artifact.get('path', '') == 'backup.tar.gz', res.json()))
        # only one artifact should be there
        artifact = artifacts[0] if len(artifacts) > 0 else {}

        return artifact.get('url', None)
    except Exception as e:
        # something has failed, but no big deal
        print(e)


def download_data(path, url):
    with open(path, 'wb') as f:
        for chunk in get(url, stream=True).iter_content(chunk_size=1024*1024*3):
            f.write(chunk)


def fetch_artifacts(offset, loop):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    res = get(f'{PROJECT_URL}?limit=100&offset={offset}')
    res.raise_for_status()
    jobs = res.json()
    sync_and_nightly_jobs = filter(is_sync_and_nightly, jobs)
    build_nums = filter(lambda x: x is not None, map(lambda job: job.get('build_num', None), sync_and_nightly_jobs))
    appended = False
    for build_num in build_nums:
        url = fetch_url(build_num)
        if url is None:
            continue
        print(f'Downloading {url}')
        # Schedule downloading in the event loop
        loop.run_in_executor(None, download_data, f'{DOWNLOAD_DIR}/{build_num}_backup.tar.gz', url)
        appended = True
    return appended


def main():
    offset = -1
    # how many times no artifacts were returned
    empty_times = 0
    # if no artifacts for three consecutive calls, bail out
    print('Starting artifacts finding and scheduling downloads')
    loop = asyncio.get_event_loop()
    while empty_times < 3:
        offset += 1
        appended = fetch_artifacts(offset * 100, loop)
        # increase empty counter, otherwise reset it to 0 to cover a gap
        empty_times += 1 if not appended else 0
    print(f'Finished finding artifacts, last offset was {offset * 100}')


if __name__ == "__main__":
   main()
