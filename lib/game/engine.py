import copy
import random

import lib.game.constants as constants
from lib.game.models import GameState


def _board_iterator(board, state_filter=None):
    for x, col in enumerate(board):
        for y, tile in enumerate(col):
            yield_it = True
            if state_filter:
                yield_it = (tile['state'] == state_filter)

            if yield_it:
                yield (x, y, tile)


class Engine(object):
    MOVE_UP = 'up'
    MOVE_DOWN = 'down'
    MOVE_LEFT = 'left'
    MOVE_RIGHT = 'right'

    VALID_MOVES = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]

    STARVATION = 'starvation'
    WALL = 'wall'
    LARGE_NUMBER = 999999

    @classmethod
    def create_game_state(cls, game_id, width, height):
        game_state = GameState(game_id=game_id)
        game_state.board = cls.create_board(width, height)
        return game_state

    @staticmethod
    def create_board(width, height):
        board = []
        for x in range(width):
            board.append([])

            for y in range(height):
                board[x].append({
                    'state': GameState.TILE_STATE_EMPTY,
                    'snake': None
                })

        return board

    @staticmethod
    def add_snakes_to_board(game_state, snakes):
        # Add snakes to .snakes
        game_state.snakes = snakes

        # Add snakes to .board
        Engine.update_snakes_on_board(game_state)

        return game_state

    @staticmethod
    def add_random_snakes_to_board(game_state, snakes):

        # Generate starting positions
        def get_quarter_dimensions(dimension):
            mid = (dimension - 1) / 2
            diff = (mid / 2) + 1
            return [mid - diff, mid, mid + diff]

        width_quarters = get_quarter_dimensions(len(game_state.board))
        height_quarters = get_quarter_dimensions(len(game_state.board[0]))

        first_four = [
            [width_quarters[0], height_quarters[0]],  # top left
            [width_quarters[2], height_quarters[0]],  # top right
            [width_quarters[2], height_quarters[2]],  # bottom right
            [width_quarters[0], height_quarters[2]]  # bottom left
        ]
        second_four = [
            [width_quarters[1], height_quarters[0]],  # mid top
            [width_quarters[2], height_quarters[1]],  # mid right
            [width_quarters[1], height_quarters[2]],  # mid bottom
            [width_quarters[0], height_quarters[1]],  # mid left
        ]

        random.shuffle(first_four)
        random.shuffle(second_four)

        starting_coords = (first_four + second_four)

        # Place snakes

        for snake, coords in zip(snakes, starting_coords):
            snake['coords'] = [coords for i in range(constants.SNAKE_STARTING_LENGTH)]

        Engine.add_snakes_to_board(game_state, snakes)

        return game_state

    @staticmethod
    def check_snake_starvation(game_state):
        for snake in copy.deepcopy(game_state.snakes):
            if game_state.turn - snake.get('last_eaten', 0) > constants.HUNGER_THRESHOLD:
                game_state.snakes.remove(snake)
                snake['died_on_turn'] = game_state.turn
                snake['killed_by'] = Engine.STARVATION
                game_state.dead_snakes.append(snake)

    @staticmethod
    def add_random_food_to_board(game_state):
        if len(game_state.food) < constants.MAX_FOOD_ON_BOARD:
            empty_tile_coords = [
                [x, y]
                for (x, y, tile) in _board_iterator(
                    game_state.board,
                    state_filter=GameState.TILE_STATE_EMPTY
                )
            ]
            if empty_tile_coords:
                Engine.add_food_to_board(game_state, random.choice(empty_tile_coords))

        return game_state

    @staticmethod
    def add_starting_food_to_board(game_state):
        def get_mid_coords(dimension):
            half = (dimension - 1) / 2
            if (dimension % 2) == 0:
                return [half, half + 1]
            return [half]

        width = len(game_state.board)
        height = len(game_state.board[0])

        for x in get_mid_coords(width):
            for y in get_mid_coords(height):
                Engine.add_food_to_board(game_state, [x, y])

        return game_state

    @staticmethod
    def add_food_to_board(game_state, food):
        game_state.food.append(food)

        Engine.set_coords(
            game_state=game_state,
            coords=food,
            state=GameState.TILE_STATE_FOOD)

        return game_state

    @classmethod
    def update_snakes_on_board(cls, game_state):
        snakes = game_state.snakes
        for snake in snakes:
            for coords in snake['coords']:
                if coords == snake['coords'][0]:
                    state = GameState.TILE_STATE_SNAKE_HEAD
                else:
                    state = GameState.TILE_STATE_SNAKE_BODY

                cls.set_coords(
                    game_state=game_state,
                    coords=coords,
                    state=state,
                    snake=snake['name'])

    @staticmethod
    def update_food_on_board(game_state):
        food = game_state.food
        for coords in food:
            Engine.set_coords(
                game_state=game_state,
                coords=coords,
                state=GameState.TILE_STATE_FOOD)

    @classmethod
    def get_default_move(cls, snake):
        head_coords, next_coords = snake['coords'][0:2]
        vector = [head_coords[0] - next_coords[0], head_coords[1] - next_coords[1]]

        if vector == [0, -1]:
            move = cls.MOVE_UP
        elif vector == [0, 1]:
            move = cls.MOVE_DOWN
        elif vector == [1, 0]:
            move = cls.MOVE_RIGHT
        elif vector == [-1, 0]:
            move = cls.MOVE_LEFT
        elif vector == [0, 0]:
            # Greg: Run into the wall right away.
            move = random.choice([cls.MOVE_LEFT, cls.MOVE_RIGHT, cls.MOVE_DOWN, cls.MOVE_UP])
        else:
            raise Exception('failed to determine default move: %s' % str(vector))

        return {
            'move': move,
            'snake_name': snake['name']
        }

    @classmethod
    def resolve_moves(cls, game_state, moves):
        # Determine what snakes and food are left on the board after this turn
        new_snakes = []
        dead_snakes = copy.deepcopy(game_state.dead_snakes)
        new_food = list(game_state.food)

        # Get moves for all snakes
        for snake in game_state.snakes:
            move = cls.get_default_move(snake)

            # Find move for this snake
            for m in moves:
                if m['snake_name'] == snake['name'] and m['move'] in cls.VALID_MOVES:
                    move = m
                    break

            action = move['move']
            snake_name = move['snake_name']

            # Copy Old Snake
            new_snake = cls.copy_snake(game_state, snake_name)

            # If the snake is dead, ignore this move
            if not new_snake:
                continue

            # Add New Head
            if action == cls.MOVE_UP:
                new_head = list(sum(x) for x in zip(new_snake['coords'][0], [0, -1]))
                new_snake['coords'].insert(0, new_head)

            if action == cls.MOVE_DOWN:
                new_head = list(sum(x) for x in zip(new_snake['coords'][0], [0, 1]))
                new_snake['coords'].insert(0, new_head)

            if action == cls.MOVE_RIGHT:
                new_head = list(sum(x) for x in zip(new_snake['coords'][0], [1, 0]))
                new_snake['coords'].insert(0, new_head)

            if action == cls.MOVE_LEFT:
                new_head = list(sum(x) for x in zip(new_snake['coords'][0], [-1, 0]))
                new_snake['coords'].insert(0, new_head)

            # Remove Tail
            new_snake['coords'].pop(-1)

            new_snakes.append(new_snake)

        # Track Snake Collisions
        kill = []       # [snake_name, snake_name]
        grow = {}       # {snake_name: grow_by, snake_name: grow_by}
        eaten = []      # [(food, coords)]

        # Check Collisions
        for snake in new_snakes:

            # Check for wall collisions
            if snake['coords'][0][0] < 0:
                kill.append(snake['name'])
                snake['killed_by'] = Engine.WALL
                continue

            if snake['coords'][0][1] < 0:
                kill.append(snake['name'])
                snake['killed_by'] = Engine.WALL
                continue

            if snake['coords'][0][0] >= len(game_state.board):
                kill.append(snake['name'])
                snake['killed_by'] = Engine.WALL
                continue

            if snake['coords'][0][1] >= len(game_state.board[0]):
                kill.append(snake['name'])
                snake['killed_by'] = Engine.WALL
                continue

            for check_snake in new_snakes:

                # Self Collision or Ignore Self
                if snake['name'] == check_snake['name']:
                    if snake['coords'][0] in check_snake['coords'][1:]:
                        kill.append(snake['name'])
                        snake['killed_by'] = check_snake['name']
                        continue
                    else:
                        continue

                # Head to Head Collision
                if snake['coords'][0] == check_snake['coords'][0]:
                    if len(snake['coords']) <= len(check_snake['coords']):
                        kill.append(snake['name'])
                        snake['killed_by'] = check_snake['name']
                        continue

                # Head to Body Collision
                if snake['coords'][0] in check_snake['coords']:
                    kill.append(snake['name'])
                    grow[check_snake['name']] = grow.get(snake['name'], 0) + int(len(snake['coords']) * constants.EAT_RATIO)
                    snake['killed_by'] = check_snake['name']
                    check_snake['kills'] = check_snake.get('kills', 0) + 1
                    continue

            if snake['coords'][0] in new_food:
                if snake['name'] not in kill:
                    eaten.append(snake['coords'][0])

                    grow[snake['name']] = grow.get(snake['name'], 0) + 1
                    snake['food_eaten'] = snake.get('food_eaten', 0) + 1

                    continue

        # Resolve Collisions
        for snake in copy.deepcopy(new_snakes):
            if snake['name'] in kill:
                new_snakes.remove(snake)
                snake['died_on_turn'] = game_state.turn
                dead_snakes.append(snake)

        for snake_name, grow_by in grow.iteritems():
            for snake in new_snakes:
                if snake['name'] == snake_name:
                    snake['last_eaten'] = game_state.turn
                    for x in range(0, grow_by):
                        snake['coords'].append(snake['coords'][-1])

        for food in copy.deepcopy(new_food):
            if food in eaten:
                new_food.remove(food)

        # Create new_game_state using new_snakes and new_food
        new_game_state = cls.create_game_state(game_state.game_id, len(game_state.board), len(game_state.board[0]))
        new_game_state.snakes = new_snakes
        new_game_state.dead_snakes = dead_snakes
        new_game_state.food = new_food

        new_game_state.turn = game_state.turn + 1

        cls.check_snake_starvation(new_game_state)

        cls.update_food_on_board(new_game_state)
        cls.update_snakes_on_board(new_game_state)

        # Add food every X turns
        if new_game_state.turn % constants.TURNS_PER_FOOD == 0:
            cls.add_random_food_to_board(new_game_state)

        # Check if the game is over
        total_snakes = len(new_game_state.snakes) + len(new_game_state.dead_snakes)
        if total_snakes == 1 and len(new_game_state.snakes) == 0:
            # Single snake games go until the end
            new_game_state.is_done = True

        elif total_snakes > 1 and len(new_game_state.snakes) <= 1:
            # Multi snake games go until one snake left
            new_game_state.is_done = True

        return new_game_state

    @staticmethod
    def copy_snake(game_state, snake_name):
        for snake in game_state.snakes:
            if snake['name'] == snake_name:
                return copy.deepcopy(snake)
        return None

    # Set Coords (x, y) to State
    @staticmethod
    def set_coords(game_state, coords, state, snake=None):
        x = coords[0]
        y = coords[1]

        tile_state = {
            'state': state,
            'snake': snake
        }
        game_state.board[x][y] = tile_state
        game_state.sanity_check()
