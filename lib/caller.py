import gevent.monkey

gevent.monkey.patch_all()

from gevent import Timeout, pool as gevent_pool

import requests
import json
import time


def _log(msg):
    print "[caller] %s" % str(msg)


class ClientTimeout(RuntimeError):
    pass


class AsyncCall(object):
    def __init__(self, payload, urls, timeout=None):
        self._payload = payload
        self._urls = urls
        self._timeout = timeout

        self._init_responses()

    def _init_responses(self):
        self._responses = {}

        # Default all responses to None
        for url in self._urls:
            self._responses[url] = None

    def _call_url(self, url):
        start = time.time()

        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(self._payload), headers=headers)
        print '----------------------'
        print response
        print '----------------------'

        if response.status_code == 200:
            try:
                data = json.loads(response.text)
            except ValueError:
                pass
            else:
                self._responses[url] = data
        else:
            _log('Failed to contact %s: %s' % (url, response.status_code))

        end = time.time()

        _log('Called %s in %.2fs' % (url, end - start))

    def _start_task(self, url):
        # Start a timeout timer if we need to

        if self._timeout:
            try:
                with Timeout(self._timeout, ClientTimeout):
                    self._call_url(url)
            except ClientTimeout:
                # Do nothing if the client times out. It's fine
                _log('Async request timed out for %s' % url)
        else:
            self._call_url(url)

    def start(self):
        start = time.time()

        self._init_responses()

        group = gevent_pool.Group()

        # Willem: we whouldn't actually need a BatchTimeout right?
        for url in self._urls:
            group.spawn(self._start_task, url)

        group.join()

        end = time.time()
        _log('Finished %s urls in %.2fs' % (len(self._urls), end - start))

        return self._responses

# # # # # # # # # # # # # # # # # # # # # #
# Test
# AsyncCall({'hello': 'world'}, [
#     'http://requestb.in/u9ti65u9?foo=1',
#     'http://requestb.in/u9ti65u9?foo=2',
#     'http://requestb.in/u9ti65u9?foo=3'
# ], 0.5).start()
