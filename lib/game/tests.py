from lib.models.game import Game
from engine import Engine, Snake

SNAKE_1 = Snake(
    name='test_snake_1',
    coords=[[2, 1], [1, 1], [0, 1]],
    url=''
)

SNAKE_2 = Snake(
    name='test_snake_2',
    coords=[[4, 1], [5, 1], [6, 1]],
    url=''
)

SNAKE_3 = Snake(
    name='test_snake_3',
    coords=[[2, 2], [2, 3], [2, 4]],
    url=''
)

SNAKE_4 = Snake(
    name='test_snake_4',
    coords=[[4, 5], [5, 5], [5, 4], [5, 3], [4, 3], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8]],
    url=''
)

SNAKE_5 = Snake(
    name='test_snake_5',
    coords=[[4, 1], [5, 1], [6, 1], [7, 1]],
    url=''
)


def test_move_east():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    g.sanity_check()

    with open('lib/game/data/move_right.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/move_right.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_move_back_on_self():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    g.sanity_check()

    with open('lib/game/data/move_right.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_WEST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/empty.out') as f:
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

    g.snakes[0].move = Engine.MOVE_EAST
    g.snakes[1].move = Engine.MOVE_WEST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/empty.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_head_to_head_uneven():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1, SNAKE_5])
    g.sanity_check()

    with open('lib/game/data/head_to_head_uneven.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g.snakes[1].move = Engine.MOVE_WEST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/head_to_head_uneven.out') as f:
        end_state = f.read().strip()
    print g.to_string().strip()
    assert(g.to_string().strip() == end_state.strip())


def test_head_to_head_with_food():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1, SNAKE_2])
    g.food.append([3, 1])
    g.sanity_check()

    with open('lib/game/data/head_to_head_with_food.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g.snakes[1].move = Engine.MOVE_WEST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/head_to_head_with_food.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())
    assert(len(g.food) == 1)


def test_head_to_body():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1, SNAKE_3])
    g.sanity_check()

    with open('lib/game/data/head_to_body.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g.snakes[1].move = Engine.MOVE_NORTH
    g = Engine.resolve_moves(g)
    g.sanity_check()

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/head_to_body.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())


def test_eat_food():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    g.food.append([3, 1])
    g.sanity_check()

    with open('lib/game/data/eat_food.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/eat_food.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())
    assert(len(g.food) == 0)


def test_trap_self():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_4])
    g.sanity_check()
    
    with open('lib/game/data/trap_self.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_NORTH
    g = Engine.resolve_moves(g)
    g.sanity_check()

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/empty.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())

def test_eat_gold():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    g.gold.append([3, 1])
    g.sanity_check()

    with open('lib/game/data/gold_test_1.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/gold_test_1.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())
    assert(len(g.gold) == 0)

def test_hit_random_wall():
    game = Game(width=10, height=10)
    g = Engine.create_game_state(game.id, game.width, game.height)
    Engine.add_snakes_to_board(g, [SNAKE_1])
    g.walls.append([3, 1])
    g.sanity_check()

    with open('lib/game/data/wall_test_1.in') as f:
        start_state = f.read().strip()

    assert(g.to_string().strip() == start_state)

    g.snakes[0].move = Engine.MOVE_EAST
    g = Engine.resolve_moves(g)
    g.sanity_check()

    with open('lib/game/data/wall_test_1.out') as f:
        end_state = f.read().strip()

    assert(g.to_string().strip() == end_state.strip())
    assert(len(g.walls) == 1)