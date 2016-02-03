import copy
import math
import random

import lib.game.constants as constants
from lib.models.game import GameState, Game


class Snake(object):
    STATUS_ALIVE = 'alive'
    STATUS_DEAD = 'dead'
    FULL_HEALTH = 100

    def __init__(self, team_id, name='', color='', head='', taunt='', coords=[]):

        super(Snake, self).__init__()

        self.team_id = team_id
        self.name = name
        self.color = color
        self.head = head
        self.taunt = taunt
        self.status = Snake.STATUS_ALIVE
        self.message = ''
        self.age = 0
        self.health = self.FULL_HEALTH
        self.coords = coords
        self.kills = 0
        self.food_eaten = 0
        self.last_eaten = 0
        self.gold = 0
        self.killed_by = ''
        self.died_on_turn = 0
        self.move = ''
        self.error = None

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'Snake[{}]'.format(self.name)

    def to_dict(self):
        return {
            'team_id': self.team_id,
            'name': self.name,
            'color': self.color,
            'head': self.head,
            'taunt': self.taunt,
            'status': self.status,
            'message': self.message,
            'age': self.age,
            'health': self.health,
            'coords': self.coords,
            'kills': self.kills,
            'food_eaten': self.food_eaten,
            'last_eaten': self.last_eaten,
            'gold': self.gold,
            'killed_by': self.killed_by,
            'died_on_turn': self.died_on_turn,
        }

    @classmethod
    def from_dict(cls, obj):
        snake = cls(obj['team_id'], obj['name'], obj['color'], obj['head'], obj['taunt'])
        snake.status = obj['status']
        snake.message = obj['message']
        snake.age = obj['age']
        snake.health = obj['health']
        snake.coords = obj['coords']
        snake.kills = obj['kills']
        snake.food_eaten = obj['food_eaten']
        snake.last_eaten = obj['last_eaten']
        snake.gold = obj['gold']
        snake.killed_by = obj['killed_by']
        snake.died_on_turn = obj['died_on_turn']

        return snake

    def move_north(self):
        new_head = list(sum(x) for x in zip(self.coords[0], [0, -1]))
        self.coords.insert(0, new_head)
        self.coords.pop(-1)

    def move_south(self):
        new_head = list(sum(x) for x in zip(self.coords[0], [0, 1]))
        self.coords.insert(0, new_head)
        self.coords.pop(-1)

    def move_east(self):
        new_head = list(sum(x) for x in zip(self.coords[0], [1, 0]))
        self.coords.insert(0, new_head)
        self.coords.pop(-1)

    def move_west(self):
        new_head = list(sum(x) for x in zip(self.coords[0], [-1, 0]))
        self.coords.insert(0, new_head)
        self.coords.pop(-1)

    def grow_by(self, grow_by):
        for x in range(0, grow_by):
            self.coords.append(self.coords[-1])


class Engine(object):
    MOVE_NORTH = 'north'
    MOVE_SOUTH = 'south'
    MOVE_WEST = 'west'
    MOVE_EAST = 'east'

    VALID_MOVES = [MOVE_NORTH, MOVE_SOUTH, MOVE_WEST, MOVE_EAST]

    STARVATION = 'starvation'
    SUICIDE = 'itself'
    WALL = 'wall'
    EDGE = 'edge'
    GOLD = 'gold victory'

    @classmethod
    def create_game_state(cls, game_id, width, height, mode=Game.MODE_CLASSIC):
        return GameState(game_id=game_id, width=width, height=height, mode=mode)

    @staticmethod
    def add_snakes_to_board(game_state, snakes):
        game_state.snakes = snakes
        return game_state

    @staticmethod
    def add_random_snakes_to_board(game_state, snakes):

        # Generate starting positions
        def get_quarter_dimensions(dimension):
            mid = (dimension - 1) / 2
            diff = (mid / 2) + 1
            return [mid - diff, mid, mid + diff]

        width_quarters = get_quarter_dimensions(game_state.width)
        height_quarters = get_quarter_dimensions(game_state.height)

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
            snake.coords = [coords for _ in range(constants.SNAKE_STARTING_LENGTH)]

        return Engine.add_snakes_to_board(game_state, snakes)

    @staticmethod
    def add_tile_to_board(game_state, tile_type):

        taken_tiles = []
        for snake in game_state.snakes:
            taken_tiles += [coord for coord in snake.coords]
            # Give every snake head a 1 move buffer (so walls dont spawn in front of them)
            taken_tiles.append([snake.coords[0][0]+1, snake.coords[0][1]])
            taken_tiles.append([snake.coords[0][0]-1, snake.coords[0][1]])
            taken_tiles.append([snake.coords[0][0], snake.coords[0][1]+1])
            taken_tiles.append([snake.coords[0][0], snake.coords[0][1]-1])

        taken_tiles += [food for food in game_state.food]
        taken_tiles += [gold for gold in game_state.gold]
        taken_tiles += [wall for wall in game_state.walls]

        empty_tile_coords = []
        for x in range(game_state.width):
            for y in range(game_state.height):
                if [x, y] not in taken_tiles:
                    empty_tile_coords.append([x, y])

        if empty_tile_coords:
            if tile_type == GameState.TILE_STATE_FOOD and len(game_state.food) < constants.MAX_FOOD_ON_BOARD:
                game_state.food.append(random.choice(empty_tile_coords))

            if tile_type == GameState.TILE_STATE_GOLD:
                game_state.gold.append(random.choice(empty_tile_coords))

            if tile_type == GameState.TILE_STATE_WALL:
                game_state.walls.append(random.choice(empty_tile_coords))

        return game_state

    @staticmethod
    def add_starting_food_to_board(game_state):
        def get_mid_coords(dimension):
            half = (dimension - 1) / 2
            if (dimension % 2) == 0:
                return [half, half + 1]
            return [half]

        for x in get_mid_coords(game_state.width):
            for y in get_mid_coords(game_state.height):
                game_state.food.append([x, y])

        return game_state

    @classmethod
    def get_default_move(cls, snake):
        head_coords, next_coords = snake.coords[0:2]
        vector = [head_coords[0] - next_coords[0], head_coords[1] - next_coords[1]]

        if vector == [0, -1]:
            move = cls.MOVE_NORTH
        elif vector == [0, 1]:
            move = cls.MOVE_SOUTH
        elif vector == [1, 0]:
            move = cls.MOVE_EAST
        elif vector == [-1, 0]:
            move = cls.MOVE_WEST
        elif vector == [0, 0]:
            # Greg: Run into the wall right away.
            move = random.choice([cls.MOVE_WEST, cls.MOVE_EAST, cls.MOVE_SOUTH, cls.MOVE_NORTH])
        else:
            raise Exception('failed to determine default move: %s' % str(vector))

        return move

    @classmethod
    def resolve_moves(cls, game_state):
        # Determine what snakes and food are left on the board after this turn
        new_snakes = []
        new_food = list(game_state.food)
        new_gold = list(game_state.gold)
        dead_snakes = copy.deepcopy(game_state.dead_snakes)

        # Determine New Snake Coords
        for snake in game_state.snakes:

            # Make sure move is valid
            if snake.move not in cls.VALID_MOVES:
                snake.move = cls.get_default_move(snake)

            # Copy Old Snake
            new_snake = copy.deepcopy(snake)

            # Move the snake
            if snake.move == cls.MOVE_NORTH:
                new_snake.move_north()
            elif snake.move == cls.MOVE_SOUTH:
                new_snake.move_south()
            elif snake.move == cls.MOVE_EAST:
                new_snake.move_east()
            elif snake.move == cls.MOVE_WEST:
                new_snake.move_west()

            # Save snake in New Position
            new_snakes.append(new_snake)

        # Track Snake Collisions
        kill = []       # [snake_name, snake_name]
        if game_state.mode == Game.MODE_ADVANCED:
            health_decay = int(math.exp(constants.HEALTH_DECAY_RATE * game_state.turn))  # Health Decay Rate this turn
        else:
            health_decay = 1

        # Check Collisions
        for snake in new_snakes:

            # Check for edge collisions
            if snake.coords[0][0] < 0:
                kill.append(snake.name)
                snake.killed_by = Engine.EDGE
                continue

            if snake.coords[0][1] < 0:
                kill.append(snake.name)
                snake.killed_by = Engine.EDGE
                continue

            if snake.coords[0][0] >= game_state.width:
                kill.append(snake.name)
                snake.killed_by = Engine.EDGE
                continue

            if snake.coords[0][1] >= game_state.height:
                kill.append(snake.name)
                snake.killed_by = Engine.EDGE
                continue

            # Check Wall Collisions
            if snake.coords[0] in game_state.walls:
                kill.append(snake.name)
                snake.killed_by = Engine.WALL
                continue

            # Check Snake Collisions
            for check_snake in new_snakes:

                # Self Collision or Ignore Self
                if snake.name == check_snake.name:
                    if snake.coords[0] in check_snake.coords[1:]:
                        kill.append(snake.name)
                        snake.killed_by = Engine.SUICIDE
                        continue
                    else:
                        continue

                # Head to Head Collision
                if snake.coords[0] == check_snake.coords[0]:
                    if len(snake.coords) <= len(check_snake.coords):
                        kill.append(snake.name)
                        snake.killed_by = check_snake.name
                        check_snake.kills += 1
                    continue

                # Head to Body Collision
                if snake.coords[0] in check_snake.coords:
                    kill.append(snake.name)
                    snake.killed_by = check_snake.name
                    check_snake.kills += 1
                    continue

            # Eat Food
            if snake.coords[0] in new_food:
                if snake.name not in kill:
                    new_food.remove(snake.coords[0])
                    snake.food_eaten += 1
                    snake.last_eaten = game_state.turn
                    snake.health = Snake.FULL_HEALTH
                    snake.grow_by(1)
                    continue

            # Collect Gold
            if snake.coords[0] in new_gold:
                if snake.name not in kill:
                    new_gold = []
                    snake.gold += 1
                    continue

        # Kill any 0 Health Snakes
        for snake in new_snakes:
            snake.health -= health_decay
            if snake.health < 1:
                kill.append(snake.name)
                snake.killed_by = Engine.STARVATION
                continue

        # Check if any snakes have achieved Gold Victory
        for snake in new_snakes:
            if snake.gold == constants.GOLD_VICTORY:
                # If so, kill off all other snakes
                for other_snake in new_snakes:
                    if other_snake.name not in kill and snake.name != other_snake.name:
                        kill.append(other_snake.name)
                        snake.killed_by = Engine.GOLD

        # Kill Off Snakes
        for snake in new_snakes:
            if snake.name in kill:
                snake.died_on_turn = game_state.turn
                dead_snakes.append(snake)

        new_snakes = [snake for snake in new_snakes if snake.name not in kill]

        # Create new_game_state using new_snakes and new_food
        new_game_state = cls.create_game_state(game_state.game_id, game_state.width, game_state.height)
        new_game_state.snakes = new_snakes
        new_game_state.dead_snakes = dead_snakes
        new_game_state.food = new_food
        new_game_state.gold = new_gold
        new_game_state.walls = game_state.walls
        new_game_state.turn = game_state.turn + 1
        new_game_state.mode = game_state.mode

        # Add food every X turns
        if new_game_state.turn % constants.TURNS_PER_FOOD == 0:
            cls.add_tile_to_board(new_game_state, GameState.TILE_STATE_FOOD)

        # Advanced Mechanics
        if new_game_state.mode == Game.MODE_ADVANCED:
            # Add gold every Y turns
            if new_game_state.turn % constants.TURNS_PER_GOLD == 0 and len(new_game_state.gold) == 0:
                cls.add_tile_to_board(new_game_state, GameState.TILE_STATE_GOLD)

            # Add gold every Z turns after turn A
            if new_game_state.turn % constants.TURNS_PER_WALL == 0 and new_game_state.turn >= constants.WALL_START_TURN:
                cls.add_tile_to_board(new_game_state, GameState.TILE_STATE_WALL)

        # Check if the game is over
        total_snakes = len(new_game_state.snakes) + len(new_game_state.dead_snakes)
        if total_snakes == 1 and len(new_game_state.snakes) == 0:
            # Single snake games go until the end
            new_game_state.is_done = True

        elif total_snakes > 1 and len(new_game_state.snakes) <= 1:
            # Multi snake games go until one snake left
            new_game_state.is_done = True

        return new_game_state
