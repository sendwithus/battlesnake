from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    def whois(self):
        return {
            'color': '#f0f087',
            'head': 'barf'
        }

    def start(self, payload):
        return {
            'taunt': 'go taunt yourself'
        }

    def move(self, payload):
        bad_tiles = []
        for snake in payload['snakes']:
            bad_tiles += snake['coords']
            if snake['name'] == 'BradSnake':
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
