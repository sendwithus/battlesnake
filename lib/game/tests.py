import os

from models import GameState


ROOT_DATA_DIR = 'lib/game/data'


def check_game_state(test_file):
    g = GameState()

    # Load game state
    with open('%s/%s.in' % (ROOT_DATA_DIR, test_file)) as f:
        g.from_string(f.read())

    # Load expected game state
    with open('%s/%s.out' % (ROOT_DATA_DIR, test_file)) as f:
        expected_output = f.read().strip()

    # TODO: APPLY STATE CHANGES

    # Get actual game state
    actual_output = g.to_string()

    assert (actual_output.strip() == expected_output.strip())


def test_game_state():
    for test_file in os.listdir(ROOT_DATA_DIR):
        if test_file.startswith('test_') and test_file.endswith('.in'):
            yield check_game_state, test_file.replace('.in', '')
