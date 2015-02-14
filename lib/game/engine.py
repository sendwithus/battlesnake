import copy
import random

from lib.game.models import GameState


class Engine(object):
    MOVE_UP = 'up'
    MOVE_DOWN = 'down'
    MOVE_LEFT = 'left'
    MOVE_RIGHT = 'right'

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
                    'snake_id': None
                })

        return board

    @staticmethod
    def add_snakes_to_board(game_state, snakes):

        for snake in snakes:
            # CURTIS: Fix collisions.
            x = random.randint(0, len(game_state.board) - 1)
            y = random.randint(0, len(game_state.board[0]) - 1)
            snake['coords'] = [(x, y), (x, y)]

            # Add snake to .snakes
            game_state.snakes.append(snake)

            # Add snake to .board
            Engine.update_snakes_on_board(game_state)

        return game_state

    @staticmethod
    def add_random_food_to_board(game_state):
        found_space = False
        while found_space is False:
            x = random.randint(0, len(game_state.board) - 1)
            y = random.randint(0, len(game_state.board[0]) - 1)
            coords = (x, y)
            found_space = True
            for snake in game_state.snakes:
                if coords in snake['coords']:
                    found_space = False
            if coords in game_state.food:
                found_space = False

        Engine.add_food_to_board(game_state, (x, y))
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
                    snake_id=snake['id'])

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
        vector = (head_coords[0] - next_coords[0], head_coords[1] - next_coords[1])

        if vector == (0, -1):
            move = cls.MOVE_UP
        elif vector == (0, 1):
            move = cls.MOVE_DOWN
        elif vector == (1, 0):
            move = cls.MOVE_RIGHT
        elif vector == (-1, 0):
            move = cls.MOVE_LEFT
        elif vector == (0, 0):
            # Greg: Run into the wall right away.
            move = random.choice([cls.MOVE_LEFT, cls.MOVE_RIGHT, cls.MOVE_DOWN, cls.MOVE_UP])
        else:
            raise Exception('failed to determine default move: %s' % str(vector))

        return {
            'move': move,
            'snake_id': snake['id']
        }

    @classmethod
    def resolve_moves(cls, game_state, moves):
        # Determine what snakes and food are left on the board after this turn
        new_snakes = []
        dead_snakes = copy.deepcopy(game_state.dead_snakes)
        new_food = list(game_state.food)

        # Get moves for all snakes
        for snake in game_state.snakes:

            # Find move for this snake
            move = cls.get_default_move(snake)
            for m in moves:
                if m['snake_id'] == snake['id']:
                    move = m
                    break

            # Apply move

            action = move['move']
            snake_id = move['snake_id']

            # Copy Old Snake
            new_snake = cls.copy_snake(game_state, snake_id)

            # If the snake is dead, ignore this move
            if not new_snake:
                continue

            # Add New Head
            if action == cls.MOVE_UP:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (0, -1)))
                new_snake['coords'].insert(0, new_head)

            if action == cls.MOVE_DOWN:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (0, 1)))
                new_snake['coords'].insert(0, new_head)

            if action == cls.MOVE_RIGHT:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (1, 0)))
                new_snake['coords'].insert(0, new_head)

            if action == cls.MOVE_LEFT:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (-1, 0)))
                new_snake['coords'].insert(0, new_head)

            # Remove Tail
            new_snake['coords'].pop(-1)

            new_snakes.append(new_snake)

        # Track Snake Collisions
        kill = []       # [snake_id, snake_id]
        grow = {}       # {snake_id: grow_by, snake_id: grow_by}
        eaten = []      # [(food, coords)]

        # Check Collisions
        for snake in new_snakes:

            # Check for wall collisions
            if snake['coords'][0][0] < 0:
                kill.append(snake['id'])
                continue

            if snake['coords'][0][1] < 0:
                kill.append(snake['id'])
                continue

            if snake['coords'][0][0] >= len(game_state.board):
                kill.append(snake['id'])
                continue

            if snake['coords'][0][1] >= len(game_state.board[0]):
                kill.append(snake['id'])
                continue

            if snake['coords'][0] in new_food:
                eaten.append(snake['coords'][0])
                grow[snake['id']] = grow.get(snake['id'], 0) + 1
                continue

            for check_snake in new_snakes:

                # Self Collision or Ignore Self
                if snake['id'] == check_snake['id']:
                    if snake['coords'][0] in check_snake['coords'][1:]:
                        kill.append(snake['id'])
                        continue
                    else:
                        continue

                # Head to Head Collision
                if snake['coords'][0] == check_snake['coords'][0]:
                    kill.append(snake['id'])
                    continue

                # Head to Body Collision
                if snake['coords'][0] in check_snake['coords']:
                    kill.append(snake['id'])
                    grow[check_snake['id']] = grow.get(snake['id'], 0) + int(len(snake['coords']) / 2)
                    continue

        # Resolve Collisions
        for snake in copy.deepcopy(new_snakes):

            if snake['id'] in kill:
                dead_snakes.append(snake)
                new_snakes.remove(snake)

        for snake_id, grow_by in grow.iteritems():
            for snake in new_snakes:
                if snake['id'] == snake_id:
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

        # Add food every 3 turns
        if new_game_state.turn % 3 == 0:
            cls.add_random_food_to_board(new_game_state)

        cls.update_snakes_on_board(new_game_state)
        cls.update_food_on_board(new_game_state)

        return new_game_state

    @staticmethod
    def copy_snake(game_state, snake_id):
        for snake in game_state.snakes:
            if snake['id'] == snake_id:
                return copy.deepcopy(snake)
        return None

    # Set Coords (x, y) to State
    @staticmethod
    def set_coords(game_state, coords, state, snake_id=None):
        x = coords[0]
        y = coords[1]

        tile_state = {
            'state': state,
            'snake_id': snake_id
        }
        game_state.board[x][y] = tile_state
        game_state.sanity_check()
