from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    def whois(self):
        return {
            'color': '#FFFFFF',
            'head': ''
        }

    def start(self, payload):
        result = validate_payload(payload)
        return {
            'taunt': 'northward bound'
        }

    def move(self, payload):
        move = 'north'
        if payload['turn'] % 4 == 0:
            move = 'west'
        if payload['turn'] % 4 == 1:
            move = 'north'
        if payload['turn'] % 4 == 2:
            move = 'east'
        if payload['turn'] % 4 == 3:
            move = 'south'
        result = validate_payload(payload)
        
        return {
            'move': move,
            'taunt': 'west is best'
        }

    def end(self, payload):
        result = validate_payload(payload)
        return {
            'taunt': 'oh no I died'
        }


def _is_coord_list(coord_list):
    if not isinstance(coord_list, list):
        return False
    else:
        for item in coord_list:
            if not isinstance(item, list) or len(item) != 2:
                return False
            for coord in item:
                if not isinstance(coord, int):
                    return False
    return True

def validate_payload(payload):
    game = payload.pop("game")

    if not isinstance(game, unicode):
        print "\n Invalid 'game' value."

    mode = payload.pop("mode")
    if not isinstance(mode, unicode):
        print "\n Invalid 'mode' value."

    turn = payload.pop("turn")
    if not isinstance(turn, int) or turn < 0:
        print "\n Invalid 'turn' value."

    height = payload.pop("height")
    if not isinstance(height, int) or height <= 0:
        print "\n Invalid 'board.height' value."

    width = payload.pop("width")
    if not isinstance(width, int) or width <= 0:
        print "\n Invalid 'board.width' value."

    snakes = payload.pop("snakes")
    for snake in snakes:
        snake_id = snake.pop("id")
        if not isinstance(snake_id, unicode):
            print "\n Invalid 'id' value."

        name = snake.pop("name")
        if not isinstance(name, unicode):
            print "\n Invalid 'name' value."

        taunt = snake.pop("taunt")
        if not isinstance(taunt, unicode):
            print "\n Invalid 'taunt' value."

        status = snake.pop("status")
        if not isinstance(status, unicode):
            print "\n Invalid 'status' value."

        message = snake.pop("message")
        if not isinstance(message, unicode):
            print "\n Invalid 'message' value."

        health = snake.pop("health")
        if not isinstance(health, int):
            print "\n Invalid 'health' value."

        coords = snake.pop("coords")
        if not _is_coord_list(coords):
            print "\n Invalid 'coords' value."

        kills = snake.pop("kills")
        if not isinstance(kills, int):
            print "\n Invalid 'kills' value."

        if mode == "advanced":
            gold = snake.pop("gold")
            if not isinstance(gold, int):
                print "\n Invalid 'gold' value."

    food = payload.pop("food")
    if not _is_coord_list(food):
        print "\n Invalid 'food' value."

    if mode == "advanced":
        gold = payload.pop("gold")
        if not _is_coord_list(gold):
            print "\n Invalid 'gold' value."

        walls = payload.pop("walls")
        if not _is_coord_list(walls):
            print "\n Invalid 'walls' value."

    if payload:
        print "\nUnexpected field remains: " + unicode(payload) + "\n"
    else:
        print "\nPayload validated.\n"

    return

