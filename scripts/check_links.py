import sys
from subprocess import run
from pathlib import Path


USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) '
    'Gecko/20100101 Firefox/70.0'
)
BUILD_DIR = Path(__file__).parent.parent / 'build'


sys.exit(run([
    'npx',
    'blcl',
    '--verbose',
    '--follow',
    '--recursive',
    '--get',  # because some sites return strange codes in response to HEAD :(
    f'--user-agent={USER_AGENT}',
    BUILD_DIR,
]).returncode)
