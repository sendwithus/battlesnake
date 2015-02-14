from lib.game.engine import Engine
from lib.game.models import Game, GameState


def _log(msg):
    print "[controller] %s" % str(msg)


def create_game(snakes, width, height):
    game = Game(width=width, height=height)
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
    if game.state != Game.STATUS_READY:
        raise Exception("[Controller] Asked to run non-ready game: %s" % game.name)
    _log("running game, game_id=%s" % game.id)
