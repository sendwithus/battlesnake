from lib.game.models import GameState


class Engine(object):
    MOVE_UP = 'up'
    MOVE_DOWN = 'down'
    MOVE_LEFT = 'left'
    MOVE_RIGHT = 'right'

    def create_game(game):

        game_state = GameState(
            game_id=game._game_id,
            width=game._width,
            height=game._height)

        return game_state

    def add_snakes_to_board(game_state, snakes):

        for snake in snakes:

            # Add snake to ._snakes
            game_state._snakes.insert(snake)

            # Add snake to ._board
            Engine.set_coords(
                game_state=game_state,
                coords=snake['coords'][0],
                state=GameState.TILE_STATE_SNAKE_HEAD,
                snake_id=snake['snake_id'])

        return game_state

    def update_snakes_on_board(game_state):
        snakes = game_state['snakes']
        for snake in snakes:
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

    def update_food_on_board(game_state):
        food = game_state['food']
        for coords in food:
            Engine.set_coords(
                game_state=game_state,
                coords=coords,
                state=GameState.TILE_STATE_FOOD)

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

            # Add New Head
            if action == Engine.MOVE_UP:
                new_snake['coords'].insert(new_snake['coords'][0] + (0, -1))
            if action == Engine.MOVE_DOWN:
                new_snake['coords'].insert(new_snake['coords'][0] + (0, 1))
            if action == Engine.MOVE_RIGHT:
                new_snake['coords'].insert(new_snake['coords'][0] + (1, 0))
            if action == Engine.MOVE_LEFT:
                new_snake['coords'].insert(new_snake['coords'][0] + (-1, 0))

            # Remove Tail
            new_snake['coords'].pop(-1)
            new_snakes.insert(new_snake)

        # Track Snake Collisions
        kill = []       # [{snake_id: snake_id, grow: length_to_grow}]
        grow = []       # [snake_id]
        eaten = []      # [(food, coords)]

        # Check Collisions
        for snake in new_snakes:
            for check_snake in new_snakes:

                # Ignore Self
                if snake['snake_id'] == check_snake['snake_id']:
                    pass

                # Head to Head Collision
                if snake['coords'][0] == check_snake['coords'][0]:
                    kill.append(snake['snake_id'])

                # Head to Body Collision
                if snake['coords'][0] in check_snake['coords']:
                    kill.append(snake['snake_id'])
                    grow.append(
                        {
                            'snake_id': snake['snake_id'],
                            'grow': len(check_snake['coords'])/2
                        }
                    )

                if snake['coords'][0] in new_food:
                    eaten.append(snake['coords'][0])
                    grow.append(
                        {
                            'snake_id': snake['snake_id'],
                            'grow': 1
                        }
                    )

        # Resolve Collisions
        for snake in new_snakes:
            if snake['snake_id'] in kill:
                print 'Kill this Snake'

            if snake['snake_id'] in grow:
                print 'Grow this Snake'

        for food in new_food:
            if food in eaten:
                print 'Remove this Food'

        # Create new_game_state using new_snakes and new_food
        new_game_state = GameState(
            game_id=game_state._game_id,
            width=len(game_state._board),
            height=len(game_state._board[0]))
        new_game_state._snakes = new_snakes
        new_game_state._food = new_food

        Engine.update_snakes_on_board(new_game_state)
        Engine.update_food_on_board(new_game_state)

        return new_game_state

    # Set Coords (x, y) to State
    def set_coords(game_state, coords, state, snake_id=None):
        x = coords[0]
        y = coords[1]

        tile_state = {
            'state': state,
            'snake_id': snake_id
        }

        game_state._board[x][y] = tile_state
        game_state._sanity_check()
