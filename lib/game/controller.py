import signal
import sys
import time

from gevent import signal as gevent_signal

import lib.ai as ai
from lib.game.engine import Engine
from lib.models.game import Game, GameState
from lib.log import get_logger


BATTLESNAKE_URL = 'http://www.battlesnake.io/play/games'

logger = get_logger(__name__)


def _update_slack(game_id, message):
    logger.slack('<%s/%s|%s> %s', BATTLESNAKE_URL, game_id, game_id, message)


def start_game(game_id, manual):
    game = Game.find_one({'_id': game_id})

    if not game:
        raise Exception('Could not find game %s' % game_id)

    if manual:
        game.state = Game.STATE_MANUAL
        game.save()
    else:
        game.mark_ready()

    return game


def rematch_game(game_id):
    game = Game.find_one({'_id': game_id})
    game_state = GameState.find({'game_id': game.id}, limit=1)[0]

    snake_urls = []
    for snake in game_state.snakes + game_state.dead_snakes:
        snake_urls.append(snake['url'])

    return create_game(snake_urls, game.width, game.height, game.turn_time)[0]


def __create_snake(url, color='', name='', head='', taunt=''):
    return {
        'url': url,
        'color': color,
        'name': name,
        'head': head,
        'taunt': taunt,
        'coords': [],
    }


def create_game(snake_urls, width, height, turn_time):
    if not snake_urls or len(snake_urls) == 0:
        raise Exception('No snake urls added. You need at least one...')

    # Fetch info about each Snake
    snakes = [
        __create_snake(
            url=snake_url,
            color=response.color,
            name=response.name,
            head=response.head
        )
        for snake_url, response
        in ai.whois(snake_urls)
    ]

    game = Game(width=width, height=height, turn_time=turn_time)
    game.insert()

    # Create the first GameState
    game_state = Engine.create_game_state(game.id, game.width, game.height)

    # Init the first GameState
    Engine.add_random_snakes_to_board(game_state, snakes)
    Engine.add_starting_food_to_board(game_state)

    # Notify snakes that we're about to start
    for snake_url, response in ai.start(snake_urls, game, snakes):
        for snake in game_state.snakes:
            if snake_url == snake['url']:
                snake['taunt'] = response.taunt

    # Save the first GameState
    game_state.insert()

    if len(snakes) > 1:
        _update_slack(game.id, '%d brave snakes enter the grid: %s' % (
            len(snakes), ', '.join([s['name'] for s in snakes]))
        )

    return game, game_state


def get_moves(game_state, timeout):
    urls = []
    for snake in game_state.snakes:
        urls.append('%s/move' % snake['url'])

    payload = {
        'game_id': game_state.game_id,
        'turn': game_state.turn,
        'board': game_state.generate_board(),
        'food': game_state.food,
        'snakes': game_state.snakes
    }

    responses = []  # AsyncCall(payload, urls, timeout).start()

    moves = []

    # For all snakes
    for snake in game_state.snakes:

        # Find the response for that snake
        for url, response in responses.items():

            # We matched! Now handle the response
            if url.startswith(snake['url']):
                if response is None:
                    # Too bad for that snake. Engine should keep it moving
                    # in current direction
                    moves.append({
                        'snake_name': snake['name'],  # Don't trust id from response
                        'move': None,
                        'taunt': '!! SNAKE ERROR !!'
                    })
                    logger.info('%s time out', snake['name'])
                else:
                    moves.append({
                        'snake_name': snake['name'],  # Don't trust id from response
                        'move': response.get('move', 'no_move'),
                        'taunt': response.get('taunt', '')
                    })

    return moves


def next_turn(game):
    game_states = GameState.find({'game_id': game.id}, limit=1)

    if len(game_states) > 0:
        game_state = game_states[0]
        moves = get_moves(game_state, game.turn_time * 5)
        next_game_state = Engine.resolve_moves(game_state, moves)
        next_game_state.insert()

        return next_game_state
    else:
        raise Exception('No GameStates found for %s' % game)


def end_game(game, game_state):
    # Finalize the game
    game.stats = generate_stats_object(game, game_state)
    game.state = Game.STATE_DONE
    game.save()

    # Notify snakes
    urls = []
    for snake in game_state.snakes:
        urls.append('%s/end' % snake['url'])

    payload = {
        'game_id': game_state.game_id
    }

    responses = []  # AsyncCall(payload, urls, game.turn_time * 5)
    # Ignore responses. Suckers.

    if (len(game_state.snakes + game_state.dead_snakes) > 1):
        lose_phrase = 'loses' if len(game_state.dead_snakes) == 1 else 'lose'
        _update_slack(game.id, 'has been decided. %s wins after %d turns! %s %s.' % (
            game.stats['winner'],
            game_state.turn,
            ', '.join([snake['name'] for snake in game_state.dead_snakes]),
            lose_phrase
        ))

    return


def run_game(game):

    def sigterm_handler(*args, **kwargs):
        if game.state == Game.STATE_PLAYING:
            game.mark_ready()
        logger.info('Handled SIGTERM for %s', game)
        sys.exit(0)

    gevent_signal(signal.SIGTERM, sigterm_handler)

    if game.state != Game.STATE_READY:
        raise Exception("Controller tried to run game that wasn't ready")

    game.state = Game.STATE_PLAYING
    game.save()

    new_game_state = None

    # We have exclusive game access now
    logger.info('Starting game: %s', game.id)

    while game.state != Game.STATE_DONE:
        start_time = time.time()

        # moves = fetch_moves_async
        game = game.refetch()

        if game.state == Game.STATE_PAUSED:
            logger.info('Paused game: %s', game)
            break

        if game.state != Game.STATE_PLAYING:
            logger.info('Abored game: %s', game)
            break

        try:
            new_game_state = next_turn(game)
        except Exception:
            logger.exception('Failed to insert game state for %s', game)
            break

        logger.info('Finished turn: %s', new_game_state)

        if new_game_state.is_done:
            end_game(game, new_game_state)

        else:
            # Wait at least
            elasped_time = time.time() - start_time
            sleep_for = max(0, float(game.turn_time) - elasped_time)
            logger.info('Sleeping for %.2f: %s', sleep_for, new_game_state.id)
            time.sleep(sleep_for)

    logger.info('Done: %s', new_game_state)


def generate_stats_object(game, game_state):
    all_snakes = []
    stats = {
        'snake_names': [],
        'snakes': [],
        'longest': None,
        'hungriest': None,
        'deadliest': None,
        'winner': None
    }

    # Reverse so 2nd place is first
    game_state.dead_snakes.reverse()

    all_snakes = game_state.snakes + game_state.dead_snakes

    longest = None
    hungriest = None
    deadliest = None

    for snake in all_snakes:
        kills = snake.get('kills', 0)
        food_eaten = snake.get('food_eaten', 0)
        length = len(snake['coords'])

        if not longest or length > len(longest['coords']):
            longest = snake

        if food_eaten > 0 and (not hungriest or food_eaten > hungriest.get('food_eaten', 0)):
            hungriest = snake

        if kills > 0 and (not deadliest or kills > deadliest.get('kills', 0)):
            deadliest = snake

        # Group all the snake names
        stats['snake_names'].append(snake['name'])

    stats['snakes'] = all_snakes

    if longest:
        stats['longest'] = longest['name']

    if deadliest:
        stats['deadliest'] = longest['name']

    if hungriest:
        stats['hungriest'] = hungriest['name']

    # Find the winner
    if len(game_state.snakes) == 1:
        stats['winner'] = game_state.snakes[0]['name']

    return stats
