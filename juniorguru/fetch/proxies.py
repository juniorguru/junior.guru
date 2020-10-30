import re

import requests

from juniorguru.models import Proxy, db


STATUS_URL = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-status.txt'
STATUS_RE = re.compile(r'''
    ([\d+\.]+)  # IP address and port
    :\s
    success  # status
''', re.VERBOSE)

LIST_URL = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
LIST_RE = re.compile(r'''
    (([\d+\.]+):\d+)  # IP address and port
    \s
    [A-Z]{2}  # country code
    -
    [NAH]  # N = No anonymity, A = Anonymity, H = High anonymity
''', re.VERBOSE)


def main():
    response = requests.get(STATUS_URL)
    response.raise_for_status()
    up = []
    for line in response.text.strip().splitlines():
        match = STATUS_RE.match(line)
        if match:
            up.append(match.group(1))

    response = requests.get(LIST_URL)
    response.raise_for_status()
    addresses = []
    for line in response.text.strip().splitlines():
        match = LIST_RE.search(line)
        if match:
            if match.group(2) in up:
                addresses.append(match.group(1))

    with db:
        Proxy.drop_table()
        Proxy.create_table()

        for address in addresses:
            Proxy.create(address=address)


if __name__ == '__main__':
    main()
