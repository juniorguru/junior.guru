import re
import sys
import time
from pathlib import Path
from subprocess import PIPE, Popen


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) '
    'Gecko/20100101 Firefox/70.0'
)
EXCLUDE_URLS = [
    '*static/images/*.png',  # local links to images
    'facebook.com/search/events/?q=english',  # HTTP_404 in response if user isn't logged in
]
EXCLUDE_REASONS = [re.compile(r) for r in [
    r'^BLC_UNKNOWN$',  # crawling protection?
    r'^ERRNO_ENOTFOUND$',  # crawling protection? can't even find the domain name
    r'^HTTP_999$',  # LinkedIn crawling protection
    r'^HTTP_429$',  # Twitter crawling protection, also https://github.com/stevenvachon/broken-link-checker/issues/198
    r'^HTTP_5\d\d$',  # server-side problem, can't do anything about that
    r'HTTP_undefined',  # :notsureif:
]]
PROJECT_DIR = Path(__file__).parent.parent
PUBLIC_DIR = PROJECT_DIR / 'public'


command = ['npx', 'blcl']
options = [
    '--verbose',
    '--follow',
    '--recursive',
    '--get',  # because some sites return strange codes in response to HEAD :(
    f'--user-agent={USER_AGENT}',
]


for url in EXCLUDE_URLS:
    options.append(f'--exclude={url}')


# Internet is flaky... retrying 3 times makes us sure the problem is consistent
attempts = 1
if '--retry' in sys.argv:
    attempts = 3


broken = None
failed = 1
for attempt in range(attempts):
    print()
    print(f'Attempt #{attempt + 1} of {attempts}')
    print('=' * 79)
    broken = set()

    with Popen(command + options + [PUBLIC_DIR], stdout=PIPE, bufsize=1,
               universal_newlines=True) as proc:
        for line in proc.stdout:
            print(line, end='')
            if 'BROKEN' in line:
                match = re.search(r'(http[^ \x1b]+)[^\(]+\(([^\)]+)\)', line)
                broken.add((match.group(1), match.group(2)))

    failed = proc.returncode
    if failed:
        time.sleep(5)
    else:
        break


# https://github.com/stevenvachon/broken-link-checker/issues/169
if broken:
    warnings = []
    errors = []
    for url, reason in broken:
        relevant_list = None
        for reason_re in EXCLUDE_REASONS:
            if reason_re.search(reason):
                relevant_list = warnings
                break
        if relevant_list is None:
            relevant_list = errors
        relevant_list.append((url, reason))

    if warnings:
        print()
        print('Links not checked')
        print('=' * 79)
        for url, reason in warnings:
            print(f'{reason}\t{url}')

    if errors:
        print()
        print('Broken links')
        print('=' * 79)
        for url, reason in errors:
            print(f'{reason}\t{url}')

    sys.exit(1 if errors else 0)
else:
    sys.exit(0)
