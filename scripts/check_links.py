import sys
from subprocess import run
from pathlib import Path


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) '
    'Gecko/20100101 Firefox/70.0'
)
EXCLUDE = [
    # BLC_UNKNOWN for no obvious reason, probably crawling protection
    'https://www.hackathon.com/city/czech-republic/praha',
]
PROJECT_DIR = Path(__file__).parent.parent
BUILD_DIR = PROJECT_DIR / 'build'


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


sys.exit(run(command + options + [BUILD_DIR]).returncode)
