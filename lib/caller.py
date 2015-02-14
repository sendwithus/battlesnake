import gevent.monkey

gevent.monkey.patch_all()

from gevent import Timeout, pool as gevent_pool
import requests
import time


class ClientTimeout(RuntimeError):
    pass


class BatchTimeout(RuntimeError):
    pass







# GREG: This should be rewritten for threading
# Also guarantee responses for each URL, None if bad response.






__results = None


def call_endpoint(payload, url, timeout=None):
    global __results

    def req(url, payload):
        global __results
        __results[url] = requests.post(url, data=payload)

    start = time.time()

    if timeout:
        with Timeout(timeout, ClientTimeout):
            req(url, payload=payload)
    else:
        req(url, payload=payload)

    end = time.time()
    print 'DONE IN %s SECONDS: %s' % ((end - start), url)


def call_endpoints_async(payload, urls, timeout=None):
    global __results
    __results = {}

    def req_batch():
        group = gevent_pool.Group()
        for url in urls:
            group.spawn(call_endpoint, payload, url)
        group.join()

    start = time.time()

    if timeout:
        with Timeout(timeout, BatchTimeout):
            req_batch()
    else:
        req_batch()

    end = time.time()
    print 'DONE ALL IN %s SECONDS' % (end - start)

    # Clear __results and return
    results = __results
    del __results
    return results
