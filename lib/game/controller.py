
import time

from lib.game.engine import Engine
from lib.caller import call_endpoints_async
from lib.game.models import Game, GameState


def _log(msg):
    print "[controller] %s" % str(msg)


def start_game(game_id, manual):
    game = Game.find_one({'_id': game_id})

    if manual:
        game.state = Game.STATE_MANUAL
        game.save()
    else:
        game.state = Game.STATE_READY
        game.save()

    return game


def create_game(snake_urls, width, height):
    game = Game(width=width, height=height)

    # Fetch snakes
    start_urls = [('%s/start' % url) for url in snake_urls]
    responses = call_endpoints_async(
        payload={
            'game_id': game.id
        },
        urls=start_urls,
        timeout=game.turn_time
    )

    snakes = []
    for snake_url in snake_urls:
        for url, response in responses.items():
            if not response or not response.status_code == 200:
                # FREAK OUT
                raise Exception('failed to contact snake: %s' % url)

            response_body = response.json()

            if url.startswith(snake_url):
                snakes.append({
                    'url': snake_url,
                    'color': response_body['color'],
                    'id': response_body['name'],
                    'name': response_body['name'],
                    'taunt': response_body['taunt']
                })

    game.insert()

    # Create the first GameState
    game_state = Engine.create_game_state(game.id, game.width, game.height)

    # Init the first GameState
    Engine.add_snakes_to_board(game_state, snakes)
    Engine.add_random_food_to_board(game_state)

    # Save the first GameState
    game_state.insert()

    return (game, game_state)


def next_turn(game, moves):
    game_states = GameState.find({'game_id': game.id})

    if len(game_states) > 0:
        game_state = game_states[0]
        next_game_state = Engine.resolve_moves(game_state, moves)
        next_game_state.insert()

        return next_game_state
    else:
        raise Exception('No GameStates found for %s' % game)


def run_game(game):
    if game.state != Game.STATE_READY:
        raise Exception("Controller tried to run game that wasn't ready")

    game.state = Game.STATE_PLAYING
    game.save()

    new_game_state = None

    # We have exclusive game access now
    _log('starting game: %s' % game.id)

    while game.state != Game.STATE_DONE:
        start_time = time.time()

        ## moves = fetch_moves_async

        try:
            new_game_state = next_turn(game, [])
        except:
            _log('failed to insert game state: %s' % new_game_state.id)
            break

        _log('finished turn: %s' % new_game_state)

        if new_game_state.is_done():
            game.state = Game.STATE_DONE
            game.save()
        else:
            # Wait at least
            elasped_time = time.time() - start_time
            sleep_for = max(0, float(game.turn_time) - elasped_time)
            _log('sleeping for %.2f: %s' % (sleep_for, new_game_state.id))
            time.sleep(sleep_for)

    _log('done: %s' % new_game_state)
