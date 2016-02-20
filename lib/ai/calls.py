import json
import time

import gevent
import requests.exceptions

from lib.ai import grequests
from lib.ai.local import create_local_snake
from lib.ai.serializers import serialize_game
from lib.log import get_logger


DEFAULT_TIMEOUT_SECONDS = 1.0

logger = get_logger(__name__)


class AIResponse(object):
    """
    Maps a snake to response properties with an optional error.
    if response.error:
        print "AI ERROR:", response.error
    else:
        print response.snake, 'wants to move', response.move
    """

    def __init__(self, snake=None, data=None, error=None):
        self.data = data
        self.error = error
        self.snake = snake

    def __getattr__(self, name):
        if self.data and name in self.data:
            return self.data[name]
        raise KeyError(name)


def __call_snakes(snakes, method, endpoint, payload, timeout_seconds):
    local_snakes = []
    remote_snakes = []

    ai_responses = []

    for snake in snakes:
        if snake.url and (snake.url.startswith('http://') or snake.url.startswith('https://')):
            remote_snakes.append(snake)
        elif snake.url and snake.url.startswith('localsnake://'):
            local_snakes.append(snake)
        else:
            ai_response = AIResponse(snake=snake)
            ai_response.error = 'Invalid URL'
            ai_responses.append(ai_response)

    # Handle remote snakes first
    ai_responses.extend(__call_remote_snakes(remote_snakes, method, endpoint, payload, timeout_seconds))
    ai_responses.extend(__call_local_snakes(local_snakes, endpoint, payload))

    return ai_responses


def __call_local_snakes(snakes, endpoint, payload):
    # Hack around whois being a root URI
    if endpoint == '':
        endpoint = 'whois'

    ai_responses = []

    for snake in snakes:
        ai_response = AIResponse(snake=snake)

        snake_name = snake.url.split('://')[1]
        local_snake = create_local_snake(snake_name)

        try:
            with gevent.Timeout(0.1):
                if payload:
                    response_data = getattr(local_snake, endpoint)(payload.copy())
                else:
                    response_data = getattr(local_snake, endpoint)()
        except gevent.Timeout:
            logger.exception('local snake timeout')
            ai_response.error = 'LOCAL SNAKE TIMEOUT'
        except:
            logger.exception('local snake error')
            ai_response.error = 'LOCAL SNAKE ERROR'
        else:
            ai_response.data = response_data

        ai_responses.append(ai_response)

    return ai_responses


def __call_remote_snakes(snakes, method, endpoint, payload, timeout_seconds):
    urls = ['%s/%s' % (snake.url, endpoint) for snake in snakes]

    if method == 'POST':
        headers = {
            'content-type': 'application/json'
        }
        reqs = [
            grequests.post(url, data=json.dumps(payload), headers=headers, timeout=timeout_seconds)
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
        - color
        - head
    """
    return __call_snakes(snakes, 'GET', '', None, timeout_seconds)


def start(game, game_state):
    """
    Response:
        - taunt
    """
    payload = serialize_game(game, game_state)
    return __call_snakes(game_state.snakes, 'POST', 'start', payload, game.turn_time)


def move(game, game_state):
    """
    Response:
        - move
        - taunt
    """
    payload = serialize_game(game, game_state)
    return __call_snakes(game_state.snakes, 'POST', 'move', payload, game.turn_time)


def end(game, game_state):
    """
    Response:
        None
    """
    all_snakes = (game_state.snakes + game_state.dead_snakes)

    payload = serialize_game(game, game_state)
    return __call_snakes(all_snakes, 'POST', 'end', payload, game.turn_time)
