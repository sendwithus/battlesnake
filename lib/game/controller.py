import signal
import sys
import time

from gevent import signal as gevent_signal

import lib.ai as ai
from lib.game.engine import Engine, Snake
from lib.log import get_logger
from lib.models.game import Game, GameState

BATTLESNAKE_URL = 'http://www.battlesnake.io/app/games'

logger = get_logger(__name__)


def _update_slack(game_id, message):
    logger.slack('<%s/%s|%s> %s', BATTLESNAKE_URL, game_id, game_id, message)


def _update_snakes(snakes, ai_responses):
    for snake in snakes:
        for ai_response in ai_responses:
            if ai_response.snake.url == snake.url:
                if ai_response.error:
                    snake.error = ai_response.error

                else:
                    snake.error = None
                    if hasattr(ai_response, 'name'):
                        snake.name = ai_response.name
                    if hasattr(ai_response, 'color'):
                        snake.color = ai_response.color
                    if hasattr(ai_response, 'head'):
                        snake.head = ai_response.head
                    if hasattr(ai_response, 'taunt'):
                        snake.taunt = ai_response.taunt
                    if hasattr(ai_response, 'move'):
                        snake.move = ai_response.move

                break


def start_game(game_id, manual=None):
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
        snake_urls.append(snake.url)

    return create_game(snake_urls, game.width, game.height, game.turn_time, game.mode)[0]


def create_game(snake_urls, width, height, turn_time, mode):
    if not snake_urls or len(snake_urls) == 0:
        raise Exception('No snake urls added. You need at least one...')

    # Create snakes and fetch whois for each
    snakes = [Snake(url=snake_url) for snake_url in snake_urls]
    _update_snakes(snakes, ai.whois(snakes))

    # Create game
    game = Game(width=width, height=height, turn_time=turn_time, mode=mode)
    game.insert()

    # Create the first GameState
    game_state = Engine.create_game_state(game.id, game.width, game.height)

    # Init the first GameState
    Engine.add_random_snakes_to_board(game_state, snakes)
    Engine.add_starting_food_to_board(game_state)

    # Notify snakes that we're about to start
    _update_snakes(game_state.snakes, ai.start(game, game_state))

    # Save the first GameState
    game_state.insert()

    if len(snakes) > 1:
        _update_slack(game.id, '%d brave snakes enter the grid: %s' % (
            len(snakes), ', '.join([s.name for s in snakes]))
        )

    return game, game_state


def next_turn(game):
    game_states = GameState.find({'game_id': game.id}, limit=1)
    if not game_states:
        raise Exception('No GameStates found for %s' % game)

    game_state = game_states[0]

    # Update taunts and moves
    _update_snakes(game_state.snakes, ai.move(game, game_state))

    next_game_state = Engine.resolve_moves(game_state)
    next_game_state.insert()

    return next_game_state


def end_game(game, game_state):
    # Notify snakes that the game is over
    ai.end(game, game_state)

    # Finalize the game
    game.stats = generate_stats_object(game, game_state)
    game.state = Game.STATE_DONE
    game.save()

    for snake in game_state.snakes:
        if snake.status == Snake.STATUS_ALIVE:
            _update_slack(game.id, '%s wins after %d turns!' % (snake.name, game_state.turn))
            break


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
        kills = snake.kills
        food_eaten = snake.food_eaten
        length = len(snake.coords)

        if not longest or length > len(longest.coords):
            longest = snake

        if food_eaten > 0 and (not hungriest or food_eaten > hungriest.food_eaten):
            hungriest = snake

        if kills > 0 and (not deadliest or kills > deadliest.kills):
            deadliest = snake

        # Group all the snake names
        stats['snake_names'].append(snake.name)

    stats['snakes'] = [snake.to_dict() for snake in all_snakes]

    if longest:
        stats['longest'] = longest.name

    if deadliest:
        stats['deadliest'] = longest.name

    if hungriest:
        stats['hungriest'] = hungriest.name

    # Find the winner
    if len(game_state.snakes) == 1:
        stats['winner'] = game_state.snakes[0].name

    return stats
