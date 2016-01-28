from flask import current_app as app
import random

from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    def whois(self):
        return {
            'name': 'Chicken Snake',
            'color': '#FFFFFF',
            'head': '/static/img/chicken.jpg',
        }

    def start(self, payload):
        return {
            'taunt': 'cluck cluck cluck'
        }

    def move(self, payload):
        turn, snakes, food = payload['turn'], payload['snakes'], payload['food']
        width, height = payload['width'], payload['height']

        board = generate_board(payload)

        strategy = choose_strategy(turn, board, snakes, food)
        result = strategy.get_action()

        if isinstance(result, tuple):
            direction, taunt = result
        else:
            direction, taunt = result, None

        # move, taunt
        return {
            'move': direction,
            'taunt': taunt,
        }

    def end(self, payload):
        return {
            'taunt': 'squaaaaaaawk!'
        }


#########################
# BOARD DATA
#########################

class Constants(object):
    NAME = 'Chicken Snake'
    URL = 'localsnake://chicken'

    UP = 'north'
    DOWN = 'south'
    LEFT = 'west'
    RIGHT = 'east'

    DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    HEAD = 'head'
    FOOD = 'food'
    BODY = 'body'
    EMPTY = 'empty'
    BOUNDARY = 'boundary'
    COLLISION = 'collision'


def generate_board(payload):
    width, height = payload['width'], payload['height']

    board = [
        [
            {'state': Constants.EMPTY}
            for y in range(height)
        ]
        for x in range(width)
    ]

    for coord in payload['food']:
        board[coord[0]][coord[1]]['state'] = Constants.FOOD

    for snake in payload['snakes']:
        for i, coord in enumerate(snake['coords']):
            if i == 0:
                board[coord[0]][coord[1]]['state'] = 'head'
            else:
                board[coord[0]][coord[1]]['state'] = 'body'
            board[coord[0]][coord[1]]['snake'] = snake['name']

    return board

def dimensions(board):
    ncols = len(board)
    nrows = len(board[0])
    return ncols, nrows

def adjacent(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def manhattan_dist(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))

def get_snake(snakes):
    for snake in snakes:
        if (snake.get('teamname') == Constants.URL or snake.get('name') == Constants.NAME):
            return snake

    raise KeyError('Failed to find snake')


#########################
# AI
#########################

def choose_strategy(turn, board, snakes, food):
    me = get_snake(snakes)
    head = me['coords'][0]
    health = me['health']
    length = len(me['coords'])

    if health > 40 and length < 4:
        # stay in the corner if we have food and haven't eaten
        strategy = CornerStrategy
    else:
        if health > 40:
            # don't collect food unless you absolutely have to
            strategy = AvoidFoodStrategy
        else:
            # prefer food when low on health
            strategy = PreferFoodStrategy

    return strategy(turn, head, health, board, snakes, food)


class BaseStrategy(object):
    def __init__(self, turn, position, health, board, snakes, food):
        self.turn = turn
        self.position = position
        self.health = health
        self.board = board
        self.snakes = [
            s for s in snakes if s['coords'][0] != self.position
        ]
        self.food = food

    def log(self, msg, *args):
        name = self.__class__.__name__
        app.logger.debug(name + ': ' + msg, *args)

    def get_action(self):
        """ return (direction, taunt | None) """
        return Constants.UP, None

    def safe_directions(self, allowed_tiles=[Constants.EMPTY, Constants.FOOD]):
        good = []
        for d in Constants.DIRECTIONS:
            safe, contents = self.check_square(d, allowed_tiles)
            if safe:
                good.append((d, contents))

        return good

    def check_square(self, direction, allowed_tiles=[Constants.EMPTY, Constants.FOOD]):
        pos = self.position
        x = pos[0]
        y = pos[1]
        ncols, nrows = dimensions(self.board)

        if direction == Constants.UP:
            y -= 1
        elif direction == Constants.DOWN:
            y += 1
        elif direction == Constants.LEFT:
            x -= 1
        else:
            x += 1

        safe, contents = True, Constants.EMPTY

        # check the boundaries
        if (x >= ncols or x < 0) or (y >= nrows or y < 0):
            return False, Constants.BOUNDARY

        # check for invalid tile according to allowed_tiles
        tile = self.board[x][y]
        contents = tile['state']

        if contents not in allowed_tiles:
            safe = False

        # check for pending collision with other snakes
        for other_snake in self.snakes:
            other_snake_pos = other_snake['coords'][0]
            if adjacent(other_snake_pos, (x, y)):
                safe = False
                contents = Constants.COLLISION

        return safe, contents


class PreferFoodStrategy(BaseStrategy):
    def get_action(self):
        safe = self.safe_directions()

        if not safe:
            return Constants.UP, 'dying'

        for direction, contents in safe:
            if contents == Constants.FOOD:
                return direction

        direction, contents = random.choice(safe)

        return direction


class AvoidFoodStrategy(BaseStrategy):
    def get_action(self):
        safe = self.safe_directions()

        if not safe:
            return Constants.UP, 'dying'

        random.shuffle(safe)

        for direction, contents in safe:
            if contents != Constants.FOOD:
                return direction

        # only food??
        direction, contents = random.choice(safe)

        return direction


class CornerStrategy(BaseStrategy):
    def get_action(self):
        safe = self.safe_directions()
        safe_dirs = [direction for direction, contents in safe]

        if not safe:
            return Constants.UP, 'dying'

        ncols, nrows = dimensions(self.board)
        corners = (
            (0, 0), (ncols - 1, 0), (0, nrows - 1), (ncols - 1, nrows - 1)
        )

        closest_corner = sorted(corners, key=lambda corner:
            manhattan_dist(self.position, corner)
        )[0]

        x, y = self.position
        cx, cy = closest_corner

        if adjacent(self.position, closest_corner):
            # stay in corner, gross logic
            if closest_corner == corners[0]:
                if x > cx and Constants.DOWN in safe_dirs:
                    return Constants.DOWN
                if y > cy and Constants.RIGHT in safe_dirs:
                    return Constants.RIGHT
            if closest_corner == corners[1]:
                if x < cx and Constants.DOWN in safe_dirs:
                    return Constants.DOWN
                if y > cy and Constants.LEFT in safe_dirs:
                    return Constants.LEFT
            if closest_corner == corners[2]:
                if x > cx and Constants.UP in safe_dirs:
                    return Constants.UP
                if y < cy and Constants.RIGHT in safe_dirs:
                    return Constants.RIGHT
            if closest_corner == corners[3]:
                if x < cx and Constants.UP in safe_dirs:
                    return Constants.UP
                if y < cy and Constants.LEFT in safe_dirs:
                    return Constants.LEFT

        # move towards corner
        for direction, contents in safe:
            if direction == Constants.LEFT and cx < x:
                return direction
            if direction == Constants.RIGHT and cx > x:
                return direction
            if direction == Constants.UP and cy < y:
                return direction
            if direction == Constants.DOWN and cy > y:
                return direction

        # can't safely move towards corner, so just move randomly
        direction, _ = random.choice(safe)

        return direction
