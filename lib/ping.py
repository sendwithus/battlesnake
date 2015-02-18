import time

import requests


PING_TIMEOUT_SECONDS = 10

PING_URLS = [
    # Server
    'http://www.battlesnake.io',

    # Example Snakes
    'http://battlesnake-go.herokuapp.com',
    'http://battlesnake-node.herokuapp.com',
    'http://battlesnake-ruby.herokuapp.com',
    'http://battlesnake-java.herokuapp.com',
    'http://battlesnake-python.herokuapp.com',

    # SWU Snakes
    'http://battlesnake-coward.herokuapp.com',
    'http://battlesnake-dylan.herokuapp.com'
]


def _log(msg):
    print "[ping] %s" % str(msg)


def ping_snakes():
    for url in PING_URLS:
        try:
            r = requests.get(url, timeout=PING_TIMEOUT_SECONDS)
            _log('%s... %s' % (url, r.status_code))
        except requests.exceptions.Timeout:
            _log('%s... TIMED OUT' % url)


def main():
    while True:
        ping_snakes()
        time.sleep(30)


if __name__ == "__main__":
    main()
