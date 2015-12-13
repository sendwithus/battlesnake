import json
import time

from lib.ai import grequests
from lib.log import get_logger


logger = get_logger(__name__)


class AIResponse(object):

    def __init__(self, data):
        self.__data = data

    def __getattr__(self, name):
        if name in self.__data:
            return self.__data[name]
        raise KeyError(name)


def __build_urls(snakes, endpoint):
    # For now, assume snakes are base URLs
    return ['%s%s' % (snake_url, endpoint) for snake_url in snakes]


def __call_urls(urls, method, payload):
    start_time = time.time()

    if method == 'POST':
        headers = {
            'content-type': 'application/json'
        }
        data = json.dumps(payload)
        requests = [grequests.post(url, data=data, headers=headers) for url in urls]
    elif method == 'GET':
        requests = [grequests.get(url) for url in urls]
    else:
        raise Exception('Unknown method %s' % method)

    responses = grequests.map(requests)

    end_time = time.time()
    logger.info("Called %d URLs in %.2fs", len(urls), end_time - start_time)

    return responses


def whois(snakes):
    urls = __build_urls(snakes, '/')
    responses = __call_urls(urls, 'GET', None)
    return [AIResponse(response.json()) for response in responses]


def start(snakes):
    urls = __build_urls(snakes, '/start')
    responses = __call_urls(urls, 'POST', {})
    return [AIResponse(response.json()) for response in responses]


def move(snakes):
    urls = __build_urls(snakes, '/move')
    responses = __call_urls(urls, 'POST', {})
    return [AIResponse(response.json()) for response in responses]


def end(snakes):
    urls = __build_urls(snakes, '/end')
    responses = __call_urls(urls, 'POST', {})
    return [AIResponse(response.json()) for response in responses]
