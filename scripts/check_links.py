import sys
import time
from subprocess import run
from pathlib import Path


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) '
    'Gecko/20100101 Firefox/70.0'
)
EXCLUDE = [
    # BLC_UNKNOWN for no obvious reason, probably crawling protection
    'hackathon.com',

    # a few redirects, then HTTP_500 for no obvious reason
    'csob.cz',

    # HTTP_404 returned to both curl and browser if user isn't logged in
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


failed = 1
for attempt in range(attempts):
    print()
    print(f'Attempt #{attempt + 1} of {attempts}')
    print('=' * 79)
    failed = run(command + options + [PUBLIC_DIR]).returncode
    if failed:
        time.sleep(5)
    else:
        break
sys.exit(failed)
