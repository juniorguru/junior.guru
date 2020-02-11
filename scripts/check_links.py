import sys
from subprocess import run
from pathlib import Path


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) '
    'Gecko/20100101 Firefox/70.0'
)
EXCLUDE = [
    # BLC_UNKNOWN for no obvious reason, probably crawling protection
    'hackathon.com',

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


sys.exit(run(command + options + [PUBLIC_DIR]).returncode)
