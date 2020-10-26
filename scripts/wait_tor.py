import time
from pathlib import Path


while 'Bootstrapped 100%' not in Path('tor.log').read_text():
    time.sleep(1)
