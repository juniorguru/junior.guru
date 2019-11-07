import sys
from subprocess import Popen, run, PIPE


server = Popen(['pipenv', 'run', 'serve'], stderr=PIPE)
returncode = 1

try:
    while True:
        if 'http://localhost:3000' in server.stderr.readline().decode('utf8'):
            break
    validate = run([
        'pylinkvalidate.py',
        '--test-outside',
        '--progress',
        '--verbose=2',
        '--header=User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0',
        'http://localhost:3000'
    ])
    returncode = validate.returncode

finally:
    server.kill()

sys.exit(returncode)
