from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    def whois(self):
        return {
            'name': 'Pac-Man',
            'color': '#000000',
            'head': 'http://www.animated-gifs.eu/leisure-games-pacman/0009.gif'
        }

    def start(self, payload):
        return {
            'taunt': 'WAKAWAKAWAKAWAKAWAKA'
        }

    def move(self, payload):
        taunt = ''
        bad_tiles = []

        for snake in payload['snakes']:
            
            if snake['name'] == 'Pac-Man':
                bad_tiles += snake['coords'][1:]
                head = snake['coords'][0]
                health = snake['health']
            else:
                bad_tiles += snake['coords']
                bad_tiles.append([snake['coords'][0][0]+1, snake['coords'][0][1]])
                bad_tiles.append([snake['coords'][0][0]-1, snake['coords'][0][1]])
                bad_tiles.append([snake['coords'][0][0], snake['coords'][0][1]+1])
                bad_tiles.append([snake['coords'][0][0], snake['coords'][0][1]-1])

        for wall in payload['walls']:
            bad_tiles.append(wall)

        smallest = 999
        target = [0, 0]
        for food in payload['food']:
            x_dis = abs(food[0] - head[0])
            y_dis = abs(food[1] - head[1])
            distance = x_dis + y_dis
            if distance < smallest:
                smallest = distance
                target = food

        if len(payload['gold']) > 0 and health > 35:
            target = payload['gold'][0]

        move = None
        if target[1] < head[1]:
            if [head[0], head[1]-1] not in bad_tiles:
                move = 'north'
        if target[1] > head[1]:
            if [head[0], head[1]+1] not in bad_tiles:
                move = 'south'
        if target[0] < head[0]:
            if [head[0]-1, head[1]] not in bad_tiles:
                move = 'west'
        if target[0] > head[0]:
            if [head[0]+1, head[1]] not in bad_tiles:
                move = 'east'

        if not move:
            if [head[0], head[1]-1] not in bad_tiles and head[1] > 0:
                move = 'north'
            if [head[0], head[1]+1] not in bad_tiles and head[1] < len(payload['board'][0]-1):
                move = 'south'
            if [head[0]-1, head[1]] not in bad_tiles and head[0] > 0:
                move = 'west'
            if [head[0]+1, head[1]] not in bad_tiles and head[0] < len(payload['board']-1):
                move = 'east'

        if payload['turn'] % 10 == 0:
            taunt = 'WAKAWAKAWAKAWAKAWAKA'

        if not move:
            taunt = "Fuck it we'll do it live!"

        return {
            'move': move,
            'taunt': taunt
        }

    def end(self, payload):
        return {
            'taunt': 'WEOWEOWEOweoweow'
        }
