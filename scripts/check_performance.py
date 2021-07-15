import json
import shutil
import sys
from multiprocessing import Pool, cpu_count
from pathlib import Path
from subprocess import run, CalledProcessError

from slugify import slugify


PUBLIC_DIR = Path(__file__).parent.parent / 'public'
LIGHTHOUSE_DIR = Path(__file__).parent.parent / 'lighthouse'

MIN_SCORES = {
    'performance': 60,
    'accessibility': 60,
    'best-practices': 90,
    'seo': 85,
}


def get_urls(public_dir):
    return [html_path_to_url(path, public_dir)
            for path in Path(public_dir).rglob('*.html')
            if '/a/' not in str(path)]


def html_path_to_url(path, public_dir):
    path = str(path).rstrip('index.html')
    path = str(Path(path).relative_to(public_dir))
    return f"https://junior.guru/{'' if path == '.' else (path + '/')}"


def url_to_report_name(url):
    return LIGHTHOUSE_DIR / slugify(url).lstrip('https-')


def url_to_json_report_path(url):
    return f'{url_to_report_name(url)}.report.json'


def url_to_html_report_path(url):
    return f'{url_to_report_name(url)}.report.html'


def get_scores(categories):
    return {score_id: int(category['score'] * 100)
            for score_id, category in categories.items()
            if score_id in MIN_SCORES.keys()}


def check_url(url):
    print(f'[CHECK] {url} → {url_to_html_report_path(url)}', file=sys.stderr)

    outputs = ['--output=json', '--output=html',
               f'--output-path={url_to_report_name(url)}']
    command = ['npx', 'lighthouse', '--quiet', '--chrome-flags=--headless']
    command += outputs + [url]
    for i in range(1, 4):
        try:
            run(command, check=True)
            break
        except CalledProcessError:
            print(f'[CHECK] attempt #{i} failed, retrying...')

    report = json.loads(Path(url_to_json_report_path(url)).read_text())
    return url, get_scores(report['categories'])


if __name__ == '__main__':
    shutil.rmtree(LIGHTHOUSE_DIR, ignore_errors=True)
    LIGHTHOUSE_DIR.mkdir(parents=True)

    pool_size = min(cpu_count(), 4)  # CircleCI declares 2, but detection reads 36
    checks = Pool(pool_size).map(check_url, get_urls(PUBLIC_DIR))
    print('')

    failing = 0
    passing = 0
    for url, scores in checks:
        for score_id, min_score in MIN_SCORES.items():
            if scores[score_id] < min_score:
                print(f'[FAIL] {url} {score_id}: {scores[score_id]} (min: {min_score})')
                failing += 1
            else:
                passing += 1

    print(f'\nFailing: {failing}\nPassing: {passing}')
    sys.exit(1 if failing else 0)
