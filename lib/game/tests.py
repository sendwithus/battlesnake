import os

from models import GameState, Game
from engine import Engine


ROOT_DATA_DIR = 'lib/game/data'
SNAKES = [
    {
        'snake_id': 'snake_1',
        'coords': [(1, 1), (1, 1)],
        'status': 'alive'
    },
    {
        'snake_id': 'snake_2',
        'coords': [(3, 3), (3, 3)],
        'status': 'alive'
    }
]

MOVES_1 = [
    {
        'snake_id': 'snake_1',
        'action': 'right'
    },
    {
        'snake_id': 'snake_2',
        'action': 'left'
    }
]

MOVES_2 = [
    {
        'snake_id': 'snake_1',
        'action': 'down'
    },
    {
        'snake_id': 'snake_2',
        'action': 'down'
    }
]

MOVES_3 = [
    {
        'snake_id': 'snake_1',
        'action': 'down'
    },
    {
        'snake_id': 'snake_2',
        'action': 'right'
    }
]

MOVES_4 = [
    {
        'snake_id': 'snake_1',
        'action': 'up'
    },
    {
        'snake_id': 'snake_2',
        'action': 'right'
    }
]

MOVES_5 = [
    {
        'snake_id': 'snake_1',
        'action': 'left'
    },
    {
        'snake_id': 'snake_2',
        'action': 'right'
    }
]

def check_game_state(test_file):
    game = Game()
    g = Engine.create_game(game)

    # Load game state
    with open('%s/%s.in' % (ROOT_DATA_DIR, test_file)) as f:
        g.from_string(f.read())

    # Load expected game state
    with open('%s/%s.out' % (ROOT_DATA_DIR, test_file)) as f:
        expected_output = f.read().strip()

    g = Engine.add_snakes_to_board(g, SNAKES)
    g._sanity_check()
    g = Engine.add_food_to_board(g, (1, 2))
    g = Engine.add_food_to_board(g, (1, 4))
    g = Engine.add_food_to_board(g, (2, 4))
    g = Engine.add_food_to_board(g, (3, 4))
    g._sanity_check()
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_1)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_1)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_1)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_2)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_2)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_3)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_3)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_3)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_3)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_1)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_1)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_4)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_4)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_4)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_4)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()
    g = Engine.resolve_moves(g, MOVES_4)
    print 'Game State Turn[' + str(g._turn) + ']\n'
    print g.to_string()


    # TODO: APPLY STATE CHANGES

    # Get actual game state
    actual_output = g.to_string()

    print 'Final Board'
    print actual_output.strip()
    print 'Expected Board'
    print expected_output.strip()

    assert (actual_output.strip() == expected_output.strip())


def test_game_state():
    for test_file in os.listdir(ROOT_DATA_DIR):
        if test_file.startswith('test_') and test_file.endswith('.in'):
            yield check_game_state, test_file.replace('.in', '')
