import gevent.monkey

gevent.monkey.patch_all()

from gevent import pool as gevent_pool
import requests
import time

__results = None


def call_endpoint(payload, url):
    global __results
    start = time.time()
    __results[url] = requests.post(url, data=payload)
    end = time.time()
    print 'DONE IN %s SECONDS: %s' % ((end - start), url)


def call_endpoints_async(payload, urls):
    global __results
    __results = {}

    group = gevent_pool.Group()

    start = time.time()

    for url in urls:
        group.spawn(call_endpoint, payload, url)

    group.join()

    end = time.time()
    print 'DONE ALL IN %s SECONDS' % (end - start)

    return __results
