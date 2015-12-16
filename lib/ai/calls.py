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


def __game_to_dict(game):
    return {
        'game': game.id,
        'mode': 'classic',
        # 'turn': game.turn,
        'height': game.height,
        'width': game.width,
    }


def __snake_to_dict(snake):
    # Note that we intentionally do not expose URL
    return {
        'name': snake['name'],
        'status': snake['status'],
        'message': snake['message'],
        'taunt': snake['taunt'],
        'age': snake['age'],
        'health': snake['health'],
        'coords': snake['coords'],
        'kills': snake['kills'],
        'food': snake['food']
    }


def __call_urls(base_urls, method, endpoint, payload):
    urls = ['%s%s' % (base_url, endpoint) for base_url in base_urls]

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

    start_time = time.time()
    responses = grequests.map(requests)
    end_time = time.time()

    logger.info("Called %d URLs in %.2fs", len(urls), end_time - start_time)

    return [
        (base_url, AIResponse(response.json()))
        for base_url, response
        in zip(base_urls, responses)
    ]


def whois(snake_urls):
    """
    Response:
        - name
        - color
        - head
    """
    return __call_urls(snake_urls, 'GET', '/', None)


def start(snake_urls, game, snakes):
    """
    Response:
        - taunt
    """
    payload = __game_to_dict(game)
    payload['snakes'] = [{'name': snake['name']} for snake in snakes]

    return __call_urls(snake_urls, 'POST', '/start', payload)


def move(snake_urls, game, game_state):
    """
    Response:
        - move
        - taunt
    """
    payload = __game_to_dict(game)
    payload['snakes'] = [__snake_to_dict(snake) for snake in game_state.snakes]
    payload['board'] = []  # TODO
    payload['food'] = []  # TODO

    return __call_urls(snake_urls, 'POST', '/move', payload)


def end(snake_urls, game, game_state):
    """
    Response:
        - taunt
    """
    payload = __game_to_dict(game)
    payload['snakes'] = [__snake_to_dict(snake) for snake in game_state.snakes]

    return __call_urls(snake_urls, 'POST', '/end', payload)
