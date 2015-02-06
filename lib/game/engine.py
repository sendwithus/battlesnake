from lib.game.models import GameState


class Engine(object):
    MOVE_UP = 'up'
    MOVE_DOWN = 'down'
    MOVE_LEFT = 'left'
    MOVE_RIGHT = 'right'

    @staticmethod
    def create_game(game):

        game_state = GameState(
            game_id=game._id,
            width=game._width,
            height=game._height)

        return game_state

    @staticmethod
    def add_snakes_to_board(game_state, snakes):

        for snake in snakes:

            # Add snake to ._snakes
            game_state._snakes.append(snake)

            # Add snake to ._board
            Engine.set_coords(
                game_state=game_state,
                coords=snake['coords'][0],
                state=GameState.TILE_STATE_SNAKE_HEAD,
                snake_id=snake['snake_id'])

        return game_state

    @staticmethod
    def add_food_to_board(game_state, food):
        game_state._food.append(food)

        Engine.set_coords(
            game_state=game_state,
            coords=food,
            state=GameState.TILE_STATE_FOOD)

        return game_state

    @staticmethod
    def update_snakes_on_board(game_state):
        snakes = game_state._snakes
        for snake in snakes:
            if snake['status'] is 'alive':
                for coords in snake['coords']:
                    if coords == snake['coords'][0]:
                        state = GameState.TILE_STATE_SNAKE_HEAD
                    else:
                        state = GameState.TILE_STATE_SNAKE_BODY

                    Engine.set_coords(
                        game_state=game_state,
                        coords=coords,
                        state=state,
                        snake_id=snake['snake_id'])

    @staticmethod
    def update_food_on_board(game_state):
        food = game_state._food
        for coords in food:
            Engine.set_coords(
                game_state=game_state,
                coords=coords,
                state=GameState.TILE_STATE_FOOD)

    @staticmethod
    def resolve_moves(game_state, moves):
        # Determine what snakes and food are left on the board after this turn
        new_snakes = []
        new_food = game_state._food

        # Determine New Snake Positions
        for move in moves:
            action = move['action']
            snake_id = move['snake_id']

            # Copy Old Snake
            new_snake = Engine.get_snake(game_state, snake_id)
            if new_snake['status'] == 'dead':
                continue

            # Add New Head
            if action == Engine.MOVE_UP:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (-1, 0)))
                new_snake['coords'].insert(0, new_head)
            if action == Engine.MOVE_DOWN:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (1, 0)))
                new_snake['coords'].insert(0, new_head)
            if action == Engine.MOVE_RIGHT:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (0, 1)))
                new_snake['coords'].insert(0, new_head)
            if action == Engine.MOVE_LEFT:
                new_head = tuple(sum(x) for x in zip(new_snake['coords'][0], (0, -1)))
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
            for check_snake in new_snakes:

                # Ignore Self
                if snake['snake_id'] == check_snake['snake_id']:
                    continue

                # Head to Head Collision
                if snake['coords'][0] == check_snake['coords'][0]:
                    kill.append(snake['snake_id'])

                # Head to Body Collision
                if snake['coords'][0] in check_snake['coords']:
                    kill.append(snake['snake_id'])
                    grow[check_snake['snake_id']] = grow.get(snake['snake_id'], 0) + len(snake['coords'])/2

                if snake['coords'][0] in new_food:
                    eaten.append(snake['coords'][0])
                    grow[snake['snake_id']] = grow.get(snake['snake_id'], 0) + 1

        # Resolve Collisions
        for i, snake in enumerate(new_snakes):

            if snake['snake_id'] in kill:
                snake['status'] = 'dead'

            if snake['snake_id'] in grow:
                for x in range(0, grow[snake['snake_id']]):
                    snake['coords'].append(snake['coords'][-1])

        for food in new_food:
            if food in eaten:
                new_food.remove(food)


        # Create new_game_state using new_snakes and new_food
        new_game_state = GameState(
            game_id=game_state._game_id,
            width=len(game_state._board),
            height=len(game_state._board[0]))
        new_game_state._snakes = new_snakes
        new_game_state._food = new_food
        new_game_state._turn = game_state._turn + 1
        Engine.update_snakes_on_board(new_game_state)
        Engine.update_food_on_board(new_game_state)

        return new_game_state

    @staticmethod
    def get_snake(game_state, snake_id):
        for snake in game_state._snakes:
            if snake['snake_id'] == snake_id:
                return snake

    # Set Coords (x, y) to State
    @staticmethod
    def set_coords(game_state, coords, state, snake_id=None):
        x = coords[0]
        y = coords[1]

        tile_state = {
            'state': state,
            'snake_id': snake_id
        }

        game_state._board[x][y] = tile_state
        game_state._sanity_check()
