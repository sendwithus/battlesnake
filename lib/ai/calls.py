import json
import time

import requests.exceptions

from lib.ai import grequests
from lib.log import get_logger


DEFAULT_TIMEOUT_SECONDS = 1.0

logger = get_logger(__name__)


class AIResponse(object):
    """
    Maps a dictionary to properties.
    if response.error:
        print "AI ERROR:", response.error
    else:
        print response.snake, response.move
    """

    def __init__(self, snake=None, data=None, error=None):
        self.data = data
        self.error = error
        self.snake = snake

    def __getattr__(self, name):
        if self.data and name in self.data:
            return self.data[name]
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


def __call_snakes(snakes, method, endpoint, payload, timeout_seconds):

    urls = ['%s%s' % (snake.url, endpoint) for snake in snakes]

    if method == 'POST':
        headers = {
            'content-type': 'application/json'
        }
        data = json.dumps(payload)
        reqs = [
            grequests.post(url, data=data, headers=headers, timeout=timeout_seconds)
            for url in urls
        ]
    elif method == 'GET':
        reqs = [
            grequests.get(url, timeout=timeout_seconds)
            for url in urls
        ]
    else:
        raise Exception('Unknown method %s' % method)

    exceptions = []

    def exception_handler(request, exception):
        exceptions.append((request, exception))

    start_time = time.time()
    responses = grequests.map(reqs, exception_handler=exception_handler)
    end_time = time.time()

    logger.info("Called %d URLs in %.2fs", len(urls), end_time - start_time)

    ai_responses = []

    # Process good responses
    for response in responses:
        for snake in snakes:
            if response.request.url.startswith(snake.url):
                # We found the snake this request is for.
                ai_response = AIResponse(snake=snake)

                if response.status_code != 200:
                    ai_response.error = 'HTTP ERROR: %s' % response.status_code
                else:
                    try:
                        response_data = response.json()
                    except ValueError:
                        ai_response.error = 'INVALID JSON RESPONSE'
                    else:
                        ai_response.data = response_data

                ai_responses.append(ai_response)
                break

    # Process exceptions
    for req, exception in exceptions:
        for snake in snakes:
            if req.url.startswith(snake.url):
                ai_response = AIResponse(snake=snake)

                try:
                    raise exception
                except requests.exceptions.Timeout:
                    ai_response.error = 'SNAKE TIMEOUT'
                except Exception as e:
                    ai_response.error = str(e)
                ai_responses.append(ai_response)
                break

    return ai_responses


def whois(snakes, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Response:
        - name
        - color
        - head
    """
    return __call_snakes(snakes, 'GET', '/', None, timeout_seconds)


def start(snakes, game, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Response:
        - taunt
    """
    payload = __game_to_dict(game)
    payload['snakes'] = [{'name': snake['name']} for snake in snakes]

    return __call_snakes(snakes, 'POST', '/start', payload, timeout_seconds)


def move(snakes, game, game_state, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Response:
        - move
        - taunt
    """
    payload = __game_to_dict(game)
    payload['snakes'] = [__snake_to_dict(snake) for snake in game_state.snakes]
    payload['board'] = []  # TODO
    payload['food'] = []  # TODO

    return __call_snakes(snakes, 'POST', '/move', payload, timeout_seconds)


def end(snakes, game, game_state, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Response:
        - taunt
    """
    payload = __game_to_dict(game)
    payload['snakes'] = [__snake_to_dict(snake) for snake in game_state.snakes]

    return __call_snakes(snakes, 'POST', '/end', payload, timeout_seconds)
