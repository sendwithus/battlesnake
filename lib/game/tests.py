from models import Game
from engine import Engine

SNAKE_1 = {
    'id': 'test_snake_1',
    'coords': [[2, 1], [1, 1]]
}

SNAKE_2 = {
    'id': 'test_snake_2',
    'coords': [[4, 1], [5, 1]]
}

SNAKE_3 = {
    'id': 'test_snake_3',
    'coords': [[2, 2], [2, 3]]
}

MOVE_RIGHT_1 = {
    'snake_id': 'test_snake_1',
    'move': Engine.MOVE_RIGHT
}

MOVE_LEFT_2 = {
    'snake_id': 'test_snake_2',
    'move': Engine.MOVE_LEFT
}

MOVE_UP_3 = {
    'snake_id': 'test_snake_3',
    'move': Engine.MOVE_UP
}


def test_move_right():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    g.sanity_check()

    with open('lib/game/data/move_right.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g = Engine.resolve_moves(g, [MOVE_RIGHT_1])
    g.sanity_check()

    with open('lib/game/data/move_right.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_head_to_head():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1, SNAKE_2])
    g.sanity_check()

    with open('lib/game/data/head_to_head.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g = Engine.resolve_moves(g, [MOVE_RIGHT_1, MOVE_LEFT_2])
    g.sanity_check()

    with open('lib/game/data/head_to_head.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_head_to_head_with_food():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1, SNAKE_2])
    Engine.add_food_to_board(g, [3, 1])
    g.sanity_check()

    with open('lib/game/data/head_to_head_with_food.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g = Engine.resolve_moves(g, [MOVE_RIGHT_1, MOVE_LEFT_2])
    g.sanity_check()

    with open('lib/game/data/head_to_head_with_food.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_head_to_body():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1, SNAKE_3])
    g.sanity_check()

    with open('lib/game/data/head_to_body.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g = Engine.resolve_moves(g, [MOVE_RIGHT_1, MOVE_UP_3])
    g.sanity_check()
    g = Engine.resolve_moves(g, [MOVE_RIGHT_1])
    g.sanity_check()

    with open('lib/game/data/head_to_body.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_eat_food():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    Engine.add_food_to_board(g, [3, 1])
    g.sanity_check()

    with open('lib/game/data/eat_food.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g = Engine.resolve_moves(g, [MOVE_RIGHT_1])
    g.sanity_check()
    g = Engine.resolve_moves(g, [MOVE_RIGHT_1])
    g.sanity_check()

    with open('lib/game/data/eat_food.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())
    assert(len(g.food) == 0)
