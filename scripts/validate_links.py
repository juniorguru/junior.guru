import sys
from subprocess import Popen, run, PIPE


server = Popen(['pipenv', 'run', 'serve'], stderr=PIPE)
returncode = 1

try:
    while True:
        if 'http://localhost:3000' in server.stderr.readline().decode('utf8'):
            break
    validate = run(['pylinkvalidate.py', 'http://localhost:3000'])
    returncode = validate.returncode

finally:
    server.kill()

sys.exit(returncode)
