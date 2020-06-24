import re
import sys
import time
from pathlib import Path
from subprocess import PIPE, Popen


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) '
    'Gecko/20100101 Firefox/70.0'
)
EXCLUDE = [
    # local links to images
    '*static/images/*.png',

    # BLC_UNKNOWN for no obvious reason, probably crawling protection
    'hackathon.com',

    # ERRNO_ENOTFOUND for no obvious reason, probably crawling protection
    # (even works locally 🤷‍♂️)
    'hackprague.com',

    # a few redirects, then HTTP_500 for no obvious reason
    'csob.cz',

    # HTTP_404 in response to both curl and browser if user isn't logged in
    'facebook.com/search/events/?q=english',
]
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


for url in EXCLUDE:
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


if broken:
    # https://github.com/stevenvachon/broken-link-checker/issues/169
    print()
    print(f'Broken links')
    print('=' * 79)
    for url, reason in broken:
        print(f'{reason}\t{url}')
sys.exit(failed)
