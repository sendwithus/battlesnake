import copy
import math
import random

from lib.ai.local import LocalSnake

SNAKE_HEAD = 'http://insomnia.rest/images/icon-small-back.png'
SNAKE_COLOR = '#423c70'


class Snake(LocalSnake):

    def whois(self):
        return {
            'color': SNAKE_COLOR,
            'head': SNAKE_HEAD
        }

    def start(self, payload):
        return {
            'taunt': 'Greg here'
        }

    def move(self, payload):
        return next_move(payload)

    def end(self, payload):
        return {
            'taunt': 'Greg out'
        }

moves = {
    0: {
        1: 'south',
        -1: 'north'
    },
    1: {0: 'east'},
    -1: {0: 'west'}
}


def _count_moves(gs, start, count=0):
    points = _get_surrounding_points(gs, start)

    if count == 0:
        gs = copy.deepcopy(gs)

    # Just so it's not too slow
    if count > 100:
        return count

    best_count = 0
    for point in points:
        if _is_on_board(gs, point) and not _is_snake(gs, point):
            # Add new position to snake
            snake = _get_snake(gs, SNAKE_NAME)
            snake['coords'].insert(0, point)

            # Mark position on board
            gs['board'][point[0]][point[1]] = {
                'state': 'body',
                'snake': snake['name']
            }

            c = _count_moves(gs, point, count + 1)
            if c > best_count:
                best_count = c

    return count + best_count


def _calc_distance(a, b):
    x_2 = (b[0] - a[0]) ** 2
    y_2 = (b[1] - a[1]) ** 2

    return math.sqrt(math.fabs(y_2 + x_2))


def _remove_diagonals(vector):
    if random.randint(0, 1) == 0:
        # Choose x
        if vector[0] != 0:
            vector[1] = 0
    else:
        # Choose y
        if vector[1] != 0:
            vector[0] = 0

    return vector


def _make_direction_vector(point):
    x = point[0]
    y = point[1]

    if x > 0:
        x = 1
    elif x < 0:
        x = -1

    if y > 0:
        y = 1
    elif y < 0:
        y = -1

    return [x, y]


def _make_point(point, vector):
    x = point[0] + vector[0]
    y = point[1] + vector[1]
    return [x, y]


def _make_move_from_points(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    vector = _make_direction_vector([x, y])
    move = _remove_diagonals(vector)
    return move


def _has_just_eaten(snake):
    return snake['coords'][-1] == snake['coords'][-2]


def _is_on_board(gs, point):
    if point[0] < 0 or point[1] < 0:
        return False

    if point[0] > len(gs['board']) - 1 or point[1] > len(gs['board'][0]) - 1:
        return False

    return True


def _is_wall(gs, point):
    return point in gs.get('walls', [])


def _is_gold(gs, point):
    return point in gs.get('gold', [])


def _is_snake(gs, point):
    for snake in gs['snakes']:
        if _has_just_eaten(snake):
            # Don't ignore tail if has just eaten
            body = snake['coords'][:]
        else:
            body = snake['coords'][:-1]

        if point in body:
            return True

    return False


def _get_surrounding_points(gs, point):
    points = [
        [point[0] + 1, point[1]],
        [point[0] - 1, point[1]],
        [point[0], point[1] + 1],
        [point[0], point[1] - 1]
    ]

    return points


def _get_safe_points(gs, start, min_moves=None):
    points = _get_surrounding_points(gs, start)
    safe_points = []
    for point in points:
        num_moves = _count_moves(gs, point)
        if min_moves > 0 and num_moves < min_moves:
            continue
        if not _is_on_board(gs, point):
            continue
        if _is_snake(gs, point):
            continue
        if _is_wall(gs, point):
            continue

        safe_points.append(point)

    if min_moves > 0 and len(safe_points) == 0:
        # If no safe points found, try again with less precision
        return _get_safe_points(gs, start, min_moves / 2)

    return safe_points


def _get_move(vector):
    return moves[vector[0]][vector[1]]


def _get_snake(gs, snake_name):
    for snake in gs['snakes']:
        if snake['name'] == snake_name:
            return snake
    return None


def _get_closest_food(gs, point):
    closest = None

    for food in gs['food']:
        if not closest:
            closest = food
        elif _calc_distance(point, food) < _calc_distance(point, closest):
            closest = food

    return closest


def _get_closest_gold(gs, point):
    closest = None

    for gold in gs.get('gold', []):
        if not closest:
            closest = gold
        elif _calc_distance(point, gold) < _calc_distance(point, closest):
            closest = gold

    return closest


def _chase_tail(gs, snake, head):
    tail = snake['coords'][-1]
    desired_move = _make_move_from_points(head, tail)
    desired_point = _make_point(head, desired_move)

    safe_points = _get_safe_points(gs, head, min_moves=0)

    # print 'SAFE POINTS', safe_points

    if desired_point not in safe_points:
        safe_point = random.choice(safe_points)
        return _make_move_from_points(head, safe_point)
    else:
        return desired_move


def _generate_board(gs):
    board = []
    for x in range(gs['width']):
        row = []
        for y in range(gs['height']):
            row.append({'state': 'empty'})
        board.append(row)

    for snake in gs['snakes']:
        for i, coord in enumerate(snake['coords']):
            if i == 0:
                board[coord[0]][coord[1]]['state'] = 'head'
            else:
                board[coord[0]][coord[1]]['state'] = 'body'
            board[coord[0]][coord[1]]['snake'] = snake['name']

    for coord in gs['food']:
        board[coord[0]][coord[1]]['state'] = 'food'

    return board


def _stay_safe(gs, snake, head):
    tail = snake['coords'][-1]

    gold = _get_closest_gold(gs, head)

    if gold is None:
        gold_distance = 999999999
    else:
        gold_distance = _calc_distance(gold, head)

    if gold_distance < 3 or random.randint(0, 15) == 0:
        dest = gold
    else:
        # TODO: Choose food that's closest to your own body (Stay tight)
        food = _get_closest_food(gs, head)

        if food is None:
            food_distance = 999999999
        else:
            food_distance = _calc_distance(food, head)

        if food_distance < 3 or random.randint(0, 15) == 0:
            dest = food
        else:
            dest = tail

    # Get a direction vector (might be diagonal)
    move = _make_move_from_points(head, dest)
    next_point = _make_point(head, move)

    my_length = len(snake['coords'])
    safe_points = _get_safe_points(gs, head, min_moves=(my_length * 2))

    # print 'SNAKE', snake['coords']
    # print 'HEAD', head
    # print 'SAFE POINTS', safe_points

    if len(safe_points) and next_point not in safe_points:
        next_point = random.choice(safe_points)
        move = _make_move_from_points(head, next_point)

    return move


def next_move(gs):
    snake = _get_snake(gs, SNAKE_NAME)

    # Legacy board
    gs['board'] = _generate_board(gs)

    # print '----------------------------------------------------------'

    # Get the closest food
    head = snake['coords'][0]

    move = _stay_safe(gs, snake, head)
    # move = _chase_tail(gs, snake, head)
    # print 'MOVE', move

    return {
        'move': _get_move(move),
        'taunt': None
    }
