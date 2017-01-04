import os
from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    SNAKE_URL = 'localsnake://' + __name__.split('.')[-1]

    def whois(self):
        return {
            'color': '#f0f087',
            'head': 'http://www.battlesnake.io/static/img/curtis.png'
        }

    def start(self, payload):
        return {
            'taunt': 'go taunt yourself'
        }

    def move(self, payload):
        __ID = os.environ.get("ID", 'c2526fb3-ff19-46ab-95c3-b7700a75329c')
        bad_tiles = []
        for snake in payload['snakes']:
            bad_tiles += snake['coords']
            if 'id' in snake and snake['id'] == __ID or 'url' in snake and snake['url'] == self.SNAKE_URL:
                head = snake['coords'][0]

        smallest = 999
        target = [0, 0]
        for food in payload['food']:
            x_dis = abs(food[0] - head[0])
            y_dis = abs(food[1] - head[1])
            distance = x_dis + y_dis
            if distance < smallest:
                smallest = distance
                target = food

        move = None
        if target[1] < head[1]:
            if [head[0], head[1]+1] not in bad_tiles:
                move = 'north'
        if target[1] > head[1]:
            if [head[0], head[1]-1] not in bad_tiles:
                move = 'south'
        if target[0] < head[0]:
            if [head[0]-1, head[1]] not in bad_tiles:
                move = 'west'
        if target[0] > head[0]:
            if [head[0]+1, head[1]] not in bad_tiles:
                move = 'east'
        return {
            'move': move,
            'taunt': 'up up and away!'
        }

    def end(self, payload):
        return {
            'taunt': 'barf I died'
        }
